import pygame
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Camera Movement Tracer")

# Set up the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Colors
black = (0, 0, 0)
trail_color = (0, 255, 0)  # Green for trail

# Trail properties
trail = []
max_trail_length = 50

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert frame to RGB (OpenCV uses BGR by default)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Detect the center of the object (for simplicity, we'll use the center of the frame)
    # You can replace this with actual object detection logic
    ball_pos = [frame.shape[1] // 2, frame.shape[0] // 2]

    # Add current ball position to the trail
    trail.append(list(ball_pos))

    # Keep trail length within limit
    if len(trail) > max_trail_length:
        trail.pop(0)

    # Clear the screen
    screen.fill(black)

    # Draw the trail
    for pos in trail:
        pygame.draw.circle(screen, trail_color, pos, 10)

    # Convert the frame to a surface
    frame_surface = pygame.surfarray.make_surface(frame)
    frame_surface = pygame.transform.rotate(frame_surface, -90)
    frame_surface = pygame.transform.flip(frame_surface, True, False)

    # Draw the frame
    screen.blit(frame_surface, (0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Release the webcam and quit Pygame
cap.release()
pygame.quit()
