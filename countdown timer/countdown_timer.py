import tkinter as tk
from tkinter import ttk
import time
import winsound
import math

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.hours = tk.StringVar(value="00")
        self.minutes = tk.StringVar(value="00")
        self.seconds = tk.StringVar(value="00")
        self.time_left = 0
        self.timer_running = False
        self.pulse_phase = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        # Time input frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20)
        
        # Hours
        ttk.Label(input_frame, text="Hours:").grid(row=0, column=0, padx=5)
        hours_entry = ttk.Entry(input_frame, textvariable=self.hours, width=5)
        hours_entry.grid(row=0, column=1, padx=5)
        
        # Minutes
        ttk.Label(input_frame, text="Minutes:").grid(row=0, column=2, padx=5)
        minutes_entry = ttk.Entry(input_frame, textvariable=self.minutes, width=5)
        minutes_entry.grid(row=0, column=3, padx=5)
        
        # Seconds
        ttk.Label(input_frame, text="Seconds:").grid(row=0, column=4, padx=5)
        seconds_entry = ttk.Entry(input_frame, textvariable=self.seconds, width=5)
        seconds_entry.grid(row=0, column=5, padx=5)
        
        # Timer display
        self.timer_label = ttk.Label(
            self.root,
            text="00:00:00",
            font=("Arial", 30)
        )
        self.timer_label.pack(pady=20)
        
        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Start button
        self.start_button = ttk.Button(
            button_frame,
            text="Start",
            command=self.start_timer
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Pause button
        self.pause_button = ttk.Button(
            button_frame,
            text="Pause",
            command=self.pause_timer,
            state="disabled"
        )
        self.pause_button.grid(row=0, column=1, padx=5)
        
        # Reset button
        self.reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer
        )
        self.reset_button.grid(row=0, column=2, padx=5)
        
    def start_timer(self):
        if not self.timer_running:
            try:
                # Get time values
                h = int(self.hours.get())
                m = int(self.minutes.get())
                s = int(self.seconds.get())
                
                # Calculate total seconds
                self.time_left = h * 3600 + m * 60 + s
                
                if self.time_left > 0:
                    self.timer_running = True
                    self.start_button.config(state="disabled")
                    self.pause_button.config(state="normal")
                    self.update_timer()
                    # Play start sound
                    winsound.Beep(1000, 100)  # 1000Hz for 100ms
            except ValueError:
                self.timer_label.config(text="Invalid Input!")
                # Play error sound
                winsound.Beep(500, 200)  # 500Hz for 200ms
                
    def pause_timer(self):
        self.timer_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        # Play pause sound
        winsound.Beep(800, 100)  # 800Hz for 100ms
        
    def reset_timer(self):
        self.timer_running = False
        self.time_left = 0
        self.hours.set("00")
        self.minutes.set("00")
        self.seconds.set("00")
        self.timer_label.config(text="00:00:00")
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        # Play reset sound
        winsound.Beep(600, 100)  # 600Hz for 100ms
        
    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            # Calculate hours, minutes, seconds
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60
            
            # Update display with animation
            time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_string)
            
            # Apply pulsing animation
            self.pulse_phase = (self.pulse_phase + 0.1) % (2 * math.pi)
            scale = 1 + 0.1 * math.sin(self.pulse_phase)
            self.timer_label.configure(font=("Arial", int(30 * scale)))
            
            # Decrease time
            self.time_left -= 1
            
            # Schedule next update
            self.root.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.timer_running = False
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled")
            self.timer_label.config(text="Time's Up!")
            # Play completion sound
            for _ in range(3):  # Play three beeps
                winsound.Beep(1000, 200)  # 1000Hz for 200ms
                self.root.after(200)  # Wait 200ms between beeps

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop() 