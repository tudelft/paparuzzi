################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../sw/ext/libopencm3/lib/efm32/efm32tg/assert.o \
../sw/ext/libopencm3/lib/efm32/efm32tg/nvic.o \
../sw/ext/libopencm3/lib/efm32/efm32tg/scb.o \
../sw/ext/libopencm3/lib/efm32/efm32tg/systick.o \
../sw/ext/libopencm3/lib/efm32/efm32tg/vector.o 

C_SRCS += \
../sw/ext/libopencm3/lib/efm32/efm32tg/vector_nvic.c 

OBJS += \
./sw/ext/libopencm3/lib/efm32/efm32tg/vector_nvic.o 

C_DEPS += \
./sw/ext/libopencm3/lib/efm32/efm32tg/vector_nvic.d 


# Each subdirectory must supply rules for building sources it contributes
sw/ext/libopencm3/lib/efm32/efm32tg/%.o: ../sw/ext/libopencm3/lib/efm32/efm32tg/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


