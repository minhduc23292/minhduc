import os
import re
import subprocess
import tempfile
from typing import Dict, List, TypedDict
from wpa_pyfi import Cell

NETWORK_INTERFACE = "wlan0"
WPA_SUPPLICANT_PATH = "/etc/wpa_supplicant/wpa_supplicant.conf"
class NetworkDict(TypedDict):
    ssid: str
    quality: float
    encrypted: bool


class NetworkOperationException(Exception):
    pass


class NetworkCheckException(Exception):
    pass

def _scan_networks() -> List[NetworkDict]:
    # Some hard-coded networks for easy debugging
    # return [
    #     {"quality": 1, "ssid": "Otani2013-05g", "encrypted": True},
    #     {"quality": 1, "ssid": "AndroidAP", "encrypted": True},
    # ]
    # Get all cells
    all_networks = Cell.all(NETWORK_INTERFACE)
    found_ssids = []
    filtered_networks = []

    for network in all_networks:
        # Filter hidden networks
        if not network.ssid:
            continue

        # De-duplicate SSID (due to duel-band wifi, or multiple AP broadcast same SSID)
        if network.ssid in found_ssids:
            continue
        found_ssids.append(network.ssid)

        filtered_networks.append(
            network.ssid
        )
    tuple_network=tuple(i for i in filtered_networks)
    # print(tuple_network)
    return tuple_network


class NetworkStatusDict(NetworkDict):
    disabled: bool
    connecting: bool


def _get_wifi_status() -> NetworkStatusDict:
    status = _get_wpa_status()

    output_status = {
        "disabled": False,
        "connecting": False,
        "ssid": "",
        "encrypted": False,
        "quality": 0,
    }

    if status["wpa_state"] == "INTERFACE_DISABLED":
        output_status["disabled"] = True
    elif status["wpa_state"] == "ASSOCIATING":
        output_status["disabled"] = False
        output_status["connecting"] = True
    elif "ssid" in status:
        output_status["ssid"] = status["ssid"]
        output_status["encrypted"] = status["key_mgmt"] != "NONE"
        output_status["quality"] = _quality_str_to_float(
            _get_ifconfig_status()["Link Quality"]
        )

    return output_status


def _get_wpa_status() -> Dict[str, str]:
    """
    Example:

    Wifi on but not connected:

        wpa_state=INACTIVE
        p2p_device_address=ba:27:eb:48:c0:2f
        address=b8:27:eb:48:c0:2f
        uuid=8b6a2a01-b772-5c93-8f1d-f13c2a41f1a1

    Wifi on and connected:

        bssid=d8:47:32:f1:81:36
        freq=2432
        ssid=Pyros-2-4
        id=0
        mode=station
        pairwise_cipher=CCMP
        group_cipher=TKIP
        key_mgmt=WPA2-PSK
        wpa_state=COMPLETED
        ip_address=192.168.0.155
        p2p_device_address=ba:27:eb:48:c0:2f
        address=b8:27:eb:48:c0:2f
        uuid=8b6a2a01-b772-5c93-8f1d-f13c2a41f1a1

    Wifi off:

        wpa_state=INTERFACE_DISABLED
        p2p_device_address=ba:27:eb:48:c0:2f
        address=b8:27:eb:48:c0:2f
        uuid=8b6a2a01-b772-5c93-8f1d-f13c2a41f1a1
    """
    try:
        wpa_output = subprocess.check_output(
            ["/usr/sbin/wpa_cli", "-i", NETWORK_INTERFACE, "status"],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        raise NetworkCheckException(e.output.strip())
    else:
        wpa_output = wpa_output.decode("utf-8")

    wpa_dict_output = {}
    for line in wpa_output.strip().split("\n"):
        key, value = line.split("=")
        wpa_dict_output[key] = value

    return wpa_dict_output


def _get_ifconfig_status() -> Dict[str, str]:
    try:
        if_output = subprocess.check_output(
            ["/usr/sbin/iwconfig", NETWORK_INTERFACE],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        raise NetworkCheckException(e.output.strip())
    else:
        if_output = if_output.decode("utf-8")

    if_dict_output = {}

    if quality_matches := re.search(r"Link Quality=(\d+/\d+)", if_output):
        if_dict_output["Link Quality"] = quality_matches[1]

    return if_dict_output


def _quality_str_to_float(quality: str) -> float:
    """Convert quality string to a ratio number

    e.g "60/70" => 0.86
    """
    current, total = quality.split("/")
    return int(current) / int(total)


def _connect(ssid: str, password: str):
    if password:
        network_block = f"""network={{
        ssid="{ssid}"
        psk="{password}"
}}"""
    else:
        network_block = f"""network={{
        ssid="{ssid}"
        key_mgmt=NONE
}}"""

    config = read_wpa_config()

    # Remove the SSID from config to override its config
    config = remove_network_from_config(ssid, config)

    # Add WPA config
    config += "\n" + network_block + "\n"

    write_wpa_config(config)
    reconfigure_wpa()


def read_wpa_config():
    with open(WPA_SUPPLICANT_PATH, "r") as config_file:
        return config_file.read()


def write_wpa_config(wpa_config: str):
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(wpa_config.encode("utf-8"))

    os.chmod(tmpfile.name, 0o644)
    subprocess.check_output(
        ["/usr/bin/sudo", "chown", "root:root", tmpfile.name],
    )
    subprocess.check_output(
        ["/usr/bin/sudo", "mv", tmpfile.name, WPA_SUPPLICANT_PATH],
    )


def reconfigure_wpa():
    """Make system load new wifi config"""
    try:
        subprocess.check_output(
            ["/usr/sbin/wpa_cli", "-i", NETWORK_INTERFACE, "reconfigure"],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        raise NetworkOperationException(e.output.strip())


def remove_network_from_config(ssid: str, wpa_config: str):
    network_regex = r"network={[^}]*\"" + re.escape(ssid) + '"[^}]*}\n?'
    wpa_config = re.sub(network_regex, "", wpa_config)

    # Clean up double newlines
    wpa_config = wpa_config.replace("\n\n", "\n")

    return wpa_config


def _disconnect(ssid: str):
    wpa_config = read_wpa_config()

    wpa_config = remove_network_from_config(ssid, wpa_config)

    write_wpa_config(wpa_config)

    reconfigure_wpa()
# if __name__=="__main__":
#     a=_scan_networks()
#     _disconnect("0tani2 T10")
#     print(a)
#     _connect("0tani2 T10 2","otani2019")