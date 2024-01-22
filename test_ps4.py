import pygame
import time

def main():
    pygame.init()
    pygame.joystick.init()

    # Check for joysticks
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("No joysticks detected")
        return

    # Initialize the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            pygame.event.pump()  # Process event queue

            # The exact axis for L2 and R2 might vary depending on the controller
            l2 = joystick.get_axis(1)  # Usually, L2 is axis 3
            r2 = joystick.get_axis(2)  # Usually, R2 is axis 4
            print(joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(2), joystick.get_axis(3), joystick.get_axis(4), joystick.get_axis(5))
            # print(f"L2: {l2:.2f}, R2: {r2:.2f}")

            time.sleep(0.2)  # Adjust the sleep time as needed

    except KeyboardInterrupt:
        print("Exiting...")
        pygame.quit()

if __name__ == "__main__":
    main()
