################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../sw/airborne/test/mcu_periph/test_sys_time.c 

OBJS += \
./sw/airborne/test/mcu_periph/test_sys_time.o 

C_DEPS += \
./sw/airborne/test/mcu_periph/test_sys_time.d 


# Each subdirectory must supply rules for building sources it contributes
sw/airborne/test/mcu_periph/%.o: ../sw/airborne/test/mcu_periph/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


