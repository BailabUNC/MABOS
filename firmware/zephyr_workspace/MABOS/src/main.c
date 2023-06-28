/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

#include <zephyr/sys/printk.h>
#include <zephyr/sys/util.h>
#include <zephyr/logging/log.h>

#include <zephyr/kernel.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/adc.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>

/* 1000 msec = 1 sec */
#define SLEEP_TIME_MS   1000

/* The devicetree node identifier for the "led0" - "led2" aliases. */
#define LED0_NODE DT_ALIAS(led0)
#define LED1_NODE DT_ALIAS(led1)
#define LED2_NODE DT_ALIAS(led2)

static const struct gpio_dt_spec led0 = GPIO_DT_SPEC_GET(LED0_NODE, gpios);
static const struct gpio_dt_spec led1 = GPIO_DT_SPEC_GET(LED1_NODE, gpios);
static const struct gpio_dt_spec led2 = GPIO_DT_SPEC_GET(LED2_NODE, gpios);

#define DT_SPEC_AND_COMMA(node_id, prop, idx) \
	ADC_DT_SPEC_GET_BY_IDX(node_id, idx),

/* Data of ADC io-channels specified in devicetree. */
static const struct adc_dt_spec adc_channels[] = {
	DT_FOREACH_PROP_ELEM(DT_PATH(zephyr_user), io_channels,
			     DT_SPEC_AND_COMMA)
};

/* Setup UART device. In devicetree file uart0 is only option */
static const struct device *uart0 = DEVICE_DT_GET(DT_NODELABEL(uart0));
struct uart_config uart_cfg = {
	.baudrate = 115200,
	.parity = UART_CFG_PARITY_NONE,
	.stop_bits = UART_CFG_STOP_BITS_1,
	.flow_ctrl = UART_CFG_FLOW_CTRL_NONE,
	.data_bits = UART_CFG_DATA_BITS_8,
};

void send_str(const struct device *uart, char *str)
{
	int msg_len = strlen(str);

	for (int i = 0; i < msg_len; i++) {
		uart_poll_out(uart, str[i]);
	}

	printk("Device %s sent: \"%s\"\n", uart->name, str);
}

int main(void)
{
	if (!gpio_is_ready_dt(&led0) || !gpio_is_ready_dt(&led1) || !gpio_is_ready_dt(&led2)) {
		return 0;
	}

	int ret0 = gpio_pin_configure_dt(&led0, GPIO_OUTPUT_ACTIVE);
        int ret1 = gpio_pin_configure_dt(&led1, GPIO_OUTPUT_ACTIVE);
        int ret2 = gpio_pin_configure_dt(&led2, GPIO_OUTPUT_ACTIVE);

	if (ret0 || ret1 || ret2 < 0) {
		return 0;
	}

        int err;
	uint32_t count = 0;
	uint16_t buf;
	struct adc_sequence sequence = {
		.buffer = &buf,
		/* buffer size in bytes, not number of samples */
		.buffer_size = sizeof(buf),
	};

	/* Configure channels individually prior to sampling. */
	for (size_t i = 0U; i < ARRAY_SIZE(adc_channels); i++) {
		if (!device_is_ready(adc_channels[i].dev)) {
			printk("ADC controller device %s not ready\n", adc_channels[i].dev->name);
			return 0;
		}

		err = adc_channel_setup_dt(&adc_channels[i]);
		if (err < 0) {
			printk("Could not setup channel #%d (%d)\n", i, err);
			return 0;
		}
	}

        /* Configure UART channel */
        int rc;
	char send_buf[64];
	rc = uart_configure(uart0, &uart_cfg);
	if (rc) {
		printk("Could not configure device %s", uart0->name);
	}

	while (1) {
                printk("ADC reading[%u]:\n", count++);
                snprintf(send_buf, 64, "Hello from device %s, num %d", uart0->name, count);
                send_str(uart0, send_buf);
                // Toggle LEDs
		//gpio_pin_toggle_dt(&led0);
  //              gpio_pin_toggle_dt(&led1);
  //              gpio_pin_toggle_dt(&led2);

                //  k_msleep(SLEEP_TIME_MS/2);
                int32_t val_mv;

                gpio_pin_toggle_dt(&led0);
                k_msleep(SLEEP_TIME_MS/2);
                (void)adc_sequence_init_dt(&adc_channels[0], &sequence);
                adc_read(adc_channels[0].dev, &sequence);

                if (adc_channels[0].channel_cfg.differential) {
                    val_mv = (int32_t)((int16_t)buf);
                } else {
                    val_mv = (int32_t)buf;
                }
                printk("%"PRId32, val_mv);
                err = adc_raw_to_millivolts_dt(&adc_channels[0],
						       &val_mv);
                printk(" = %"PRId32" mV\n", val_mv);

                gpio_pin_toggle_dt(&led0);
                gpio_pin_toggle_dt(&led1);
                k_msleep(SLEEP_TIME_MS/2);
                (void)adc_sequence_init_dt(&adc_channels[0], &sequence);
                adc_read(adc_channels[0].dev, &sequence);

                if (adc_channels[0].channel_cfg.differential) {
                    val_mv = (int32_t)((int16_t)buf);
                } else {
                    val_mv = (int32_t)buf;
                }
                printk("%"PRId32, val_mv);
                err = adc_raw_to_millivolts_dt(&adc_channels[0],
						       &val_mv);
                printk(" = %"PRId32" mV\n", val_mv);

                gpio_pin_toggle_dt(&led1);
                gpio_pin_toggle_dt(&led2);
                k_msleep(SLEEP_TIME_MS/2);
                (void)adc_sequence_init_dt(&adc_channels[0], &sequence);
                adc_read(adc_channels[0].dev, &sequence);

                if (adc_channels[0].channel_cfg.differential) {
                    val_mv = (int32_t)((int16_t)buf);
                } else {
                    val_mv = (int32_t)buf;
                }
                printk("%"PRId32, val_mv);
                err = adc_raw_to_millivolts_dt(&adc_channels[0],
						       &val_mv);
                printk(" = %"PRId32" mV\n", val_mv);
                gpio_pin_toggle_dt(&led2);
  //              for (size_t i = 0U; i < ARRAY_SIZE(adc_channels); i++) {
		//	int32_t val_mv;

		//	printk("- %s, channel %d: ",
		//	       adc_channels[i].dev->name,
		//	       adc_channels[i].channel_id);

		//	(void)adc_sequence_init_dt(&adc_channels[i], &sequence);

		//	err = adc_read(adc_channels[i].dev, &sequence);
		//	if (err < 0) {
		//		printk("Could not read (%d)\n", err);
		//		continue;
		//	}

		//	/*
		//	 * If using differential mode, the 16 bit value
		//	 * in the ADC sample buffer should be a signed 2's
		//	 * complement value.
		//	 */
		//	if (adc_channels[i].channel_cfg.differential) {
		//		val_mv = (int32_t)((int16_t)buf);
		//	} else {
		//		val_mv = (int32_t)buf;
		//	}
		//	printk("%"PRId32, val_mv);
		//	err = adc_raw_to_millivolts_dt(&adc_channels[i],
		//				       &val_mv);
		//	/* conversion to mV may not be supported, skip if not */
		//	if (err < 0) {
		//		printk(" (value in mV not available)\n");
		//	} else {
		//		printk(" = %"PRId32" mV\n", val_mv);
		//	}
		//}
		//k_msleep(SLEEP_TIME_MS/2);
	}
	return 0;
}
