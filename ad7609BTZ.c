#include <wiringPi.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define p_standby 6
#define p_cs 23
#define p_clock 11
#define p_convstab 9
#define p_dataA 8
#define p_dataB 7
#define p_reset 10
#define p_busy 24
#define p_1stData 25
#define p_range 5
#define  p_os0 13
#define  p_os1 19
#define  p_os2 26
#define  sen1_en 21
float xferFactor = 20/(pow(2,17)); // 20=2x10, 2 mean the voltage is devided by 2 so we must multiple by 2.
float *res=NULL;
struct timespec gettime_now;
//int num_chanel=6;
unsigned long long current_time_ns ()
{
//	struct timespec gettime_now;
	clock_gettime(CLOCK_REALTIME, &gettime_now);
    return(gettime_now.tv_sec * 1000000000 + gettime_now.tv_nsec);
}
void delay_ns(unsigned long  num_of_ns){
    unsigned long long start_time=current_time_ns();
    while((current_time_ns()-start_time) < num_of_ns)
    {
    continue;
    }
}
//unsigned int pow2(int a){
//    int i=1;
//    while(pow(2,i)<a)
//        i+=1;
//    return (pow(2,(i+1))+2);
//    }

long _twosComp(long long _val){
	if ((_val & (1 << 17)) != 0)
		_val = _val - (1 << 18);
	return _val;
}
float transferFunction(long long reading){
	return (xferFactor*_twosComp(reading));
}
void ADCreset(){
	digitalWrite(p_reset,HIGH);
	delay_ns(20);
	digitalWrite(p_reset,LOW);
    delay_ns(20);
	}
void delayvuvo(int n)
{
for(int _k=0; _k<n; _k++)
    continue;
}

void init(){
	wiringPiSetupGpio();
	ADCreset();

	pinMode(p_standby, OUTPUT);
	pinMode(p_reset, OUTPUT);
	pinMode(p_convstab, OUTPUT);
	pinMode(p_cs, OUTPUT);
	pinMode(p_clock, OUTPUT);
	pinMode(p_os0, OUTPUT);
	pinMode(p_os1, OUTPUT);
	pinMode(p_os2, OUTPUT);
	pinMode(p_range, OUTPUT);
    pinMode(sen1_en, OUTPUT);


	pinMode(p_dataA, INPUT);
	pinMode(p_dataB, INPUT);
	pinMode(p_busy, INPUT);
	pinMode(p_1stData, INPUT);
    // pullUpDnControl(p_dataA, PUD_DOWN);
    // pullUpDnControl(p_dataB, PUD_DOWN);

	// pullUpDnControl(p_convstab, PUD_UP);
	// pullUpDnControl(p_cs, PUD_UP);
	// pullUpDnControl(p_clock, PUD_UP);
	// pullUpDnControl(p_reset, PUD_DOWN);
	pullUpDnControl(p_busy, PUD_DOWN);
    // pullUpDnControl(sen1_en, PUD_DOWN);
    // pullUpDnControl(p_standby, PUD_DOWN);

    digitalWrite(p_convstab,HIGH);
    digitalWrite(p_convstab,HIGH);
    digitalWrite(p_cs,HIGH);
    digitalWrite(p_cs,HIGH);
	digitalWrite(p_range,HIGH);
	digitalWrite(p_range,HIGH);
    digitalWrite(p_standby,LOW);
	digitalWrite(p_standby,LOW);
    digitalWrite(p_os0,HIGH);
	digitalWrite(p_os0,HIGH);
    digitalWrite(p_os1,LOW);
	digitalWrite(p_os1,LOW);
    digitalWrite(p_os2,LOW);
	digitalWrite(p_os2,LOW);
    digitalWrite(sen1_en,HIGH);
    digitalWrite(sen1_en,HIGH);
    digitalWrite(p_clock,HIGH);
    digitalWrite(p_clock,HIGH);

}

void stanby_mode(){
    digitalWrite(p_range,HIGH);
	digitalWrite(p_range,HIGH);
    delay_ns(1000);
    digitalWrite(p_standby,LOW);
	digitalWrite(p_standby,LOW);
    delay_ns(1000);
}

void wake_up(){
    digitalWrite(p_standby,HIGH);
	digitalWrite(p_standby,HIGH);
    delay_ns(1000);
    digitalWrite(p_range,LOW);
	digitalWrite(p_range,LOW);

    delay_ns(200000);

}

float * ADCread(int num_samples, int sample_rate, int num_chanel){
    wake_up();
    int _half= num_chanel/2;
    // printf("num_chanel: %d\n", _half);
    float *containerA, *containerB, *result_arr;
    containerA=(float*)malloc(_half*sizeof(float));
    containerB=(float*)malloc(_half*sizeof(float));
    result_arr=(float*)malloc(num_chanel*sizeof(float));
    // printf("size of containerA: %d\n", sizeof(containerA));
    // printf("size of result_arr: %d\n", sizeof(result_arr));
    // printf("size of float: %d\n", sizeof(float));
    unsigned long long read_window = (unsigned long long)(1000000000 / sample_rate); // nanoseconds
    float *tem_arr=(float*)malloc((num_chanel*num_samples+1)*sizeof(float));
    unsigned long long t0=current_time_ns();
    for(int _k=0; _k<num_samples; _k++){
        while ((current_time_ns() - t0) < read_window * _k)
            {}
        digitalWrite(p_convstab,LOW);
        digitalWrite(p_convstab,LOW);
        delay_ns(25);
        digitalWrite(p_convstab,HIGH);
        digitalWrite(p_convstab,HIGH);
        delay_ns(20);

        while (digitalRead(p_busy) == 1)
                {}

        digitalWrite(p_cs,LOW);
        digitalWrite(p_cs,LOW);
        delay_ns(10);

        for(int _c=0; _c<_half; _c++){
            long long _A = 0, _B = 0;
            for(int _i=0; _i<18; _i++){ //Clock low to cleck the data to DoutA/B
                digitalWrite(p_clock,LOW);
                digitalWrite(p_clock,LOW);
                delay_ns(10);
                _A +=  digitalRead(p_dataA)<<(17-_i);
                _B +=  digitalRead(p_dataB)<<(17-_i);
                digitalWrite(p_clock,HIGH);
                digitalWrite(p_clock,HIGH);
                delay_ns(26);
            }
            containerA[_c] = transferFunction(_A);
            containerB[_c] = transferFunction(_B);
        }

        digitalWrite(p_cs,HIGH);
        digitalWrite(p_cs,HIGH);
        delay_ns(10);
        memcpy(result_arr,containerA, _half*sizeof(float));
        memcpy(&result_arr[_half],containerB, _half*sizeof(float)); // can test lai

        memcpy(&tem_arr[num_chanel*_k], result_arr, num_chanel*sizeof(float));
	}
    float actual_sample_rate= (float)(1000000000 / ((current_time_ns() - t0)/num_samples));
    tem_arr[num_chanel*num_samples]=actual_sample_rate;
	res=tem_arr;
    free(containerA);
    free(containerB);
    stanby_mode();
    // printf("len buffer: %d\n", num_samples);
	return(res);

}

void freeme(float *ptr)
{
    // printf("freeing address: %p\n", ptr);
    if (ptr != NULL)
        free(ptr);
}

void turn_on_24v(){
    digitalWrite(sen1_en,HIGH);
    digitalWrite(sen1_en,HIGH);
    delay_ns(20);
}

void turn_off_24v(){
    digitalWrite(sen1_en,LOW);
    digitalWrite(sen1_en,LOW);
    delay_ns(20);
}