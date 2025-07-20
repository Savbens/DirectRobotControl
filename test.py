import random, time

def external_data_generator(self):
        while True:
            if self.running:
                # скорость влияет на амплитуду колебаний
                base = self.current_speed
                noise = random.uniform(-10, 10)
                value = max(0, min(100, base + noise))
                self.queue_out.put(value)
            time.sleep(0.5)
