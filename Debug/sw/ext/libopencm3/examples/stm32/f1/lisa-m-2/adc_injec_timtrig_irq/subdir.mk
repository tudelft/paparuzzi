################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../sw/ext/libopencm3/examples/stm32/f1/lisa-m-2/adc_injec_timtrig_irq/adc_injec_timtrig_irq.c 

OBJS += \
./sw/ext/libopencm3/examples/stm32/f1/lisa-m-2/adc_injec_timtrig_irq/adc_injec_timtrig_irq.o 

C_DEPS += \
./sw/ext/libopencm3/examples/stm32/f1/lisa-m-2/adc_injec_timtrig_irq/adc_injec_timtrig_irq.d 


# Each subdirectory must supply rules for building sources it contributes
sw/ext/libopencm3/examples/stm32/f1/lisa-m-2/adc_injec_timtrig_irq/%.o: ../sw/ext/libopencm3/examples/stm32/f1/lisa-m-2/adc_injec_timtrig_irq/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


