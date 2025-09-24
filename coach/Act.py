# Act Component: Provide feedback to the user

import mediapipe as mp
import cv2
import numpy as np
import random
import pyttsx3
import pygame



# Act Component: Visualization to motivate user, visualization such as the skeleton and debugging information.
# Things to add: Other graphical visualization, a proper GUI, more verbal feedback
class Act:

    def __init__(self):
        # Balloon size and transition tracking for visualization
        self.image = cv2.imread("images/leave.png", cv2.IMREAD_UNCHANGED)
        self.transition_count = 0
        self.round_count = 0
        self.max_transitions = 6
        self.total_transitions = 0



        self.engine = pyttsx3.init()
        file_path = r"C:\Users\daisy\Documents\GitHub\Foundations-of-I-Tech---Week-2\audio\1 Introduction Part 1.wav"

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.motivating_index = 0
        # Preload feedback M4A files
        self.feedback_files = {
            'motivating': [
                'audio/goodjob1.wav', #1
                'audio/goodjob2.wav', #2
                'audio/goodjob3.wav',
                'audio/transition.wav',
                'audio/almost2.wav', #4
                'audio/almost3.wav', #5
            ]}

        # Handles balloon inflation and reset after explosion

    def play_audio(self, file_path):
        if not pygame.mixer.music.get_busy():  # only play if no audio is already playing
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

    def handle_balloon_inflation(self):
        """
        Increases the size of the balloon with each successful repetition.
        """
        self.transition_count += 1
        self.total_transitions += 1
        # Calculate the current round
        self.round_count = self.total_transitions // self.max_transitions
        clip = self.feedback_files['motivating'][self.motivating_index]
        self.motivating_index = (self.motivating_index + 1) % len(self.feedback_files['motivating'])
        self.play_audio(clip)




    def reset_balloon(self):
        """
        Resets the balloon after it explodes.
        """

        self.transition_count = 0
        # Play "end" audio before restarting
        end_audio = r"audio/end.wav"  # <- place your file here
        self.play_audio(end_audio)

        # Create explosion fragments with random sizes and positions


    def visualize_balloon(self):
        if self.transition_count >= 6:
            self.reset_balloon()
        img = np.full((500, 500, 3), (220, 245, 245), dtype=np.uint8)
        # Choose which image to display
        if self.transition_count < 4:
            display_image = self.image  # first image
        elif self.transition_count < 6:
            if not hasattr(self, 'second_image'):
                self.second_image = cv2.imread("images/carrot.png", cv2.IMREAD_UNCHANGED)
            display_image = self.second_image


        # Resize the image based on transition_count (like balloon size)
        scale = 0.15 + (self.transition_count * 0.08)
        new_w = int(display_image.shape[1] * scale)
        new_h = int(display_image.shape[0] * scale)

        # Clamp size so it never exceeds canvas
        new_w = min(new_w, img.shape[1])
        new_h = min(new_h, img.shape[0])

        # Resize properly after clamping
        resized_img = cv2.resize(display_image, (new_w, new_h))

        # Center placement
        x_offset = (img.shape[1] - new_w) // 2
        y_offset = (img.shape[0] - new_h) // 2
        # Split alpha and color channels
        alpha = resized_img[:, :, 3] / 255.0  # alpha channel
        rgb_carrot = resized_img[:, :, :3]  # RGB channels

        # Alpha blending into 3-channel canvas
        for c in range(3):
            img[y_offset:y_offset + resized_img.shape[0], x_offset:x_offset + resized_img.shape[1], c] = (
                    alpha * rgb_carrot[:, :, c] + (1 - alpha) * img[y_offset:y_offset + resized_img.shape[0],
                                                                x_offset:x_offset + resized_img.shape[1], c]
            )
        # Overlay text
        cv2.putText(img, f'Repetitions: {self.transition_count}', (50, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, f"Carrots grown: {self.round_count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
        cv2.imshow('Grow a carrot!', img)
        cv2.waitKey(1)


    def provide_feedback(self, decision, frame, joints, elbow_angle_mvg):
        """
        Displays the skeleton and some text using open cve.

        :param decision: The decision in which state the user is from the think component.
        :param frame: The currently processed frame form the webcam.
        :param joints: The joints extracted from mediapipe from the current frame.
        :param elbow_angle_mvg: The moving average from the left elbow angle.

        """

        mp.solutions.drawing_utils.draw_landmarks(frame, joints.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        # Define the number and text to display
        number = elbow_angle_mvg

        
        # Set the position, font, size, color, and thickness for the text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = .9
        font_color = (0, 0, 0)  # White color in BGR
        thickness = 2



        # Define the position for the number and text
        text_position = (50, 50)
        text = "Water the plant!"
        # Draw the text on the image
        cv2.putText(frame,text, text_position, font, font_scale, font_color, thickness)

        # Display the frame (for debugging purposes)
        cv2.imshow('Sport Coaching Program', frame)
