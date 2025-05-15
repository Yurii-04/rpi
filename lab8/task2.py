import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import datetime
import requests
import os
import threading
import time
from PIL import Image, ImageTk

# Constants
DEFAULT_CITY = "Kyiv"
API_KEY = "e88ff847f75e96b61790417313f59cf5"
VIDEO_DIR = "videos"
WEATHER_CHECK_INTERVAL_MINUTES = 30


class WeatherCameraApp:
    def __init__(self, root):
        """Initialize the application with the root window"""
        self.root = root
        self.root.title("Weather Reminders & Camera Management")
        self.root.geometry("1000x600")

        # Initialize variables
        self.init_camera_variables()
        self.init_weather_variables()
        
        # Create UI
        self.setup_ui()
        
        # Ensure video directory exists
        self.ensure_video_directory()

    def init_camera_variables(self):
        """Initialize camera-related variables"""
        self.camera = None
        self.is_recording = False
        self.recording_thread = None
        self.video_writer = None
        self.current_frame = None
        self.showing_camera = False
        self.camera_thread = None
        self.camera_should_run = False

    def init_weather_variables(self):
        """Initialize weather-related variables"""
        self.reminders = []
        self.weather_check_thread = None
        self.weather_check_running = False
        self.city = DEFAULT_CITY

    def setup_ui(self):
        """Setup the main UI components"""
        # Create the main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        self.reminders_tab = ttk.Frame(self.notebook)
        self.camera_tab = ttk.Frame(self.notebook)
        self.videos_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.reminders_tab, text="Weather Reminders")
        self.notebook.add(self.camera_tab, text="Camera Control")
        self.notebook.add(self.videos_tab, text="Video Management")

        # Setup each tab
        self.setup_reminders_tab()
        self.setup_camera_tab()
        self.setup_videos_tab()

        # Bind closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def ensure_video_directory(self):
        """Create videos directory if it doesn't exist"""
        if not os.path.exists(VIDEO_DIR):
            os.makedirs(VIDEO_DIR)

    def setup_reminders_tab(self):
        # Left frame for adding reminders
        left_frame = ttk.LabelFrame(self.reminders_tab, text="Add Weather Reminder")
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        # Weather condition frame
        weather_frame = ttk.Frame(left_frame)
        weather_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(weather_frame, text="City:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.city_entry = ttk.Entry(weather_frame)
        self.city_entry.insert(0, self.city)
        self.city_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(weather_frame, text="Weather Condition:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.weather_condition = ttk.Combobox(weather_frame, values=["Rain", "Snow", "Clear", "Clouds", "Thunderstorm",
                                                                     "Drizzle", "Fog", "Mist", "Haze", "Any"])
        self.weather_condition.current(9)  # Default to "Any"
        self.weather_condition.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(weather_frame, text="Temperature Condition:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.temp_condition = ttk.Combobox(weather_frame, values=["Above", "Below", "Any"])
        self.temp_condition.current(2)  # Default to "Any"
        self.temp_condition.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(weather_frame, text="Temperature (°C):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.temp_value = ttk.Entry(weather_frame)
        self.temp_value.insert(0, "0")
        self.temp_value.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Reminder message
        message_frame = ttk.Frame(left_frame)
        message_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(message_frame, text="Reminder Message:").pack(anchor="w", padx=5, pady=5)
        self.reminder_message = tk.Text(message_frame, height=5, width=30)
        self.reminder_message.pack(fill="x", padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Add Reminder", command=self.add_reminder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Check Weather Now", command=self.check_weather).pack(side=tk.LEFT, padx=5)

        self.weather_auto_check_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(button_frame, text="Auto-check weather (every 30 min)",
                        variable=self.weather_auto_check_var,
                        command=self.toggle_weather_check).pack(side=tk.LEFT, padx=5)

        # Right frame for displaying reminders
        right_frame = ttk.LabelFrame(self.reminders_tab, text="Weather Reminders List")
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)

        # Reminders listbox with scrollbar
        scrollbar = ttk.Scrollbar(right_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.reminders_listbox = tk.Listbox(right_frame, yscrollcommand=scrollbar.set, height=15)
        self.reminders_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.reminders_listbox.yview)

        # Current weather display
        weather_display = ttk.LabelFrame(right_frame, text="Current Weather")
        weather_display.pack(fill="x", padx=5, pady=5)

        self.weather_info = ttk.Label(weather_display, text="No weather data. Click 'Check Weather Now'")
        self.weather_info.pack(padx=5, pady=5)

        # Delete button
        ttk.Button(right_frame, text="Delete Selected Reminder",
                   command=self.delete_reminder).pack(pady=5)

    def setup_camera_tab(self):
        # Camera preview frame
        preview_frame = ttk.LabelFrame(self.camera_tab, text="Camera Preview")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a label for camera status
        self.camera_status_label = ttk.Label(preview_frame, text="Camera is stopped. Click 'Start Camera' to begin.")
        self.camera_status_label.pack(padx=10, pady=10)

        # Camera controls
        controls_frame = ttk.Frame(self.camera_tab)
        controls_frame.pack(fill="x", padx=10, pady=10)

        self.camera_button = ttk.Button(controls_frame, text="Start Camera", command=self.toggle_camera)
        self.camera_button.pack(side=tk.LEFT, padx=5)

        self.record_button = ttk.Button(controls_frame, text="Start Recording", command=self.toggle_recording,
                                        state=tk.DISABLED)
        self.record_button.pack(side=tk.LEFT, padx=5)

        self.recording_label = ttk.Label(controls_frame, text="")
        self.recording_label.pack(side=tk.LEFT, padx=5)

        # Camera options
        options_frame = ttk.LabelFrame(self.camera_tab, text="Camera Options")
        options_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(options_frame, text="Camera Device:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.camera_device = ttk.Entry(options_frame)
        self.camera_device.insert(0, "0")  # Default camera device
        self.camera_device.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Add detect cameras button
        ttk.Button(options_frame, text="Detect Cameras",
                   command=self.detect_cameras).grid(row=0, column=2, padx=5, pady=5)

        self.camera_info_label = ttk.Label(options_frame, text="")
        self.camera_info_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        
        # Available cameras list
        self.cameras_listbox = tk.Listbox(options_frame, height=3)
        self.cameras_listbox.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.cameras_listbox.bind('<Double-1>', self.select_camera_from_list)

    def setup_videos_tab(self):
        # Video list frame
        list_frame = ttk.LabelFrame(self.videos_tab, text="Recorded Videos")
        list_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        # Video listbox with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.videos_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.videos_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.videos_listbox.yview)

        # Buttons frame
        buttons_frame = ttk.Frame(list_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(buttons_frame, text="Refresh List",
                   command=self.refresh_video_list).pack(side=tk.LEFT, padx=5)

        ttk.Button(buttons_frame, text="Play Selected",
                   command=self.play_selected_video).pack(side=tk.LEFT, padx=5)

        ttk.Button(buttons_frame, text="Delete Selected",
                   command=self.delete_selected_video).pack(side=tk.LEFT, padx=5)

        # Initially populate the videos list
        self.refresh_video_list()

    def add_reminder(self):
        """Add a new weather reminder"""
        # Get inputs
        weather_cond = self.weather_condition.get()
        temp_cond = self.temp_condition.get()
        temp_value = self.temp_value.get()
        message = self.reminder_message.get("1.0", tk.END).strip()
        city = self.city_entry.get().strip()

        # Validate inputs
        if not self.validate_reminder_inputs(message, temp_cond, temp_value):
            return

        # Create and add reminder
        reminder = self.create_reminder(city, weather_cond, temp_cond, temp_value, message)
        self.reminders.append(reminder)

        # Update UI
        self.add_reminder_to_listbox(reminder)
        self.clear_reminder_inputs()
        
        # Show confirmation
        messagebox.showinfo("Success", "Reminder added successfully")

        # Update the default city
        self.city = city
    
    def validate_reminder_inputs(self, message, temp_cond, temp_value):
        """Validate reminder input fields"""
        if not message:
            messagebox.showerror("Error", "Please enter a reminder message")
            return False

        if temp_cond != "Any" and not temp_value.replace(".", "").replace("-", "").isdigit():
            messagebox.showerror("Error", "Please enter a valid temperature value")
            return False
            
        return True
    
    def create_reminder(self, city, weather_cond, temp_cond, temp_value, message):
        """Create a reminder object from inputs"""
        return {
            "city": city,
            "weather_condition": weather_cond,
            "temp_condition": temp_cond,
            "temp_value": float(temp_value) if temp_cond != "Any" else None,
            "message": message,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def add_reminder_to_listbox(self, reminder):
        """Add a reminder to the listbox UI"""
        # Create display text
        display_text = f"{reminder['city']} - {reminder['weather_condition']}"
        if reminder['temp_condition'] != "Any":
            display_text += f", {reminder['temp_condition']} {reminder['temp_value']}°C"
        
        # Truncate message if too long
        message_preview = reminder['message'][:30]
        if len(reminder['message']) > 30:
            message_preview += "..."
            
        display_text += f": {message_preview}"
        
        # Add to listbox
        self.reminders_listbox.insert(tk.END, display_text)
    
    def clear_reminder_inputs(self):
        """Clear reminder input fields"""
        self.reminder_message.delete("1.0", tk.END)

    def delete_reminder(self):
        """Delete the selected reminder"""
        selected = self.reminders_listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "Please select a reminder to delete")
            return

        # Delete from model and UI
        idx = selected[0]
        self.reminders_listbox.delete(idx)
        self.reminders.pop(idx)
        
        # Show confirmation
        messagebox.showinfo("Success", "Reminder deleted successfully")

    def check_weather(self):
        """Check weather for the current city and update UI"""
        # Get city from input
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return

        try:
            # Get weather data
            weather_data = self.fetch_weather_data(city)
            if not weather_data:
                return
                
            # Extract weather information
            weather_info = self.extract_weather_info(weather_data)
            
            # Update UI with weather information
            self.update_weather_display(city, weather_info)
            
            # Check for matching reminders
            self.check_reminders(city, weather_info['condition'], weather_info['temperature'])
            
        except Exception as e:
            error_msg = f"An error occurred while checking weather: {str(e)}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)

    def fetch_weather_data(self, city):
        """Fetch weather data from the API for given city"""
        print(f"Fetching weather data for {city}")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                error_msg = f"Failed to get weather data: {response.json().get('message', 'Unknown error')}"
                messagebox.showerror("API Error", error_msg)
                return None
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not connect to weather service: {str(e)}")
            return None
    
    def extract_weather_info(self, data):
        """Extract relevant weather information from API response"""
        weather_condition = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        return {
            'condition': weather_condition,
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed
        }
    
    def update_weather_display(self, city, weather_info):
        """Update the weather display in the UI"""
        weather_text = (
            f"City: {city}\n"
            f"Weather: {weather_info['condition']}\n"
            f"Temperature: {weather_info['temperature']}°C\n"
            f"Humidity: {weather_info['humidity']}%\n"
            f"Wind Speed: {weather_info['wind_speed']} m/s"
        )
        self.weather_info.config(text=weather_text)

    def check_reminders(self, city, weather_condition, temperature):
        """Check if any reminders match the current weather conditions"""
        matched_reminders = self.get_matching_reminders(city, weather_condition, temperature)
        
        if matched_reminders:
            self.show_reminder_notifications(matched_reminders)
    
    def get_matching_reminders(self, city, weather_condition, temperature):
        """Get list of reminders matching the current weather conditions"""
        matched_reminders = []
        
        for reminder in self.reminders:
            # Skip reminders for different cities
            if reminder["city"].lower() != city.lower():
                continue
                
            # Check if weather condition matches
            weather_matches = (
                reminder["weather_condition"] == "Any" or 
                reminder["weather_condition"] == weather_condition
            )
            
            # Check if temperature matches
            temp_matches = True
            if reminder["temp_condition"] == "Above":
                temp_matches = temperature > reminder["temp_value"]
            elif reminder["temp_condition"] == "Below":
                temp_matches = temperature < reminder["temp_value"]
                
            # If both weather and temperature match, add to matched reminders
            if weather_matches and temp_matches:
                matched_reminders.append(reminder["message"])
                
        return matched_reminders
    
    def show_reminder_notifications(self, reminders):
        """Show notifications for matched reminders"""
        reminder_text = "\n\n".join(reminders)
        messagebox.showinfo(
            "Weather Reminder", 
            f"Weather conditions match your reminders:\n\n{reminder_text}"
        )

    def toggle_weather_check(self):
        """Toggle automatic weather checking"""
        if self.weather_auto_check_var.get():
            # Start automatic checking
            self.start_weather_check_thread()
        else:
            # Stop automatic checking
            self.stop_weather_check_thread()
    
    def start_weather_check_thread(self):
        """Start the automatic weather checking thread"""
        self.weather_check_running = True
        self.weather_check_thread = threading.Thread(
            target=self.automatic_weather_check,
            daemon=True
        )
        self.weather_check_thread.start()
        print("Started automatic weather checking")
    
    def stop_weather_check_thread(self):
        """Stop the automatic weather checking thread"""
        self.weather_check_running = False
        print("Stopped automatic weather checking")

    def automatic_weather_check(self):
        """Periodically check weather in a background thread"""
        while self.weather_check_running:
            # Check weather
            self.root.after(0, self.check_weather)
            
            # Wait until next check or until stopped
            for _ in range(WEATHER_CHECK_INTERVAL_MINUTES * 60):
                if not self.weather_check_running:
                    break
                time.sleep(1)

    def toggle_camera(self):
        """Start or stop the camera in a separate window"""
        if not self.showing_camera:
            # Start camera
            try:
                device_id = self.get_camera_device_id()
                if device_id is None:
                    return
                    
                # Start camera window in a separate thread
                self.start_camera_thread(device_id)
                
            except Exception as e:
                self.handle_camera_error(f"Error starting camera: {str(e)}")
        else:
            # Stop camera
            self.stop_camera()
    
    def get_camera_device_id(self):
        """Get and validate the camera device ID from the UI"""
        try:
            device_id = int(self.camera_device.get())
            print(f"Using camera with device_id: {device_id}")
            return device_id
        except ValueError:
            messagebox.showerror("Error", "Camera device ID must be a number")
            return None
            
    def start_camera_thread(self, device_id):
        """Start the camera thread and update UI accordingly"""
        # Create a separate thread for the camera
        self.camera_should_run = True
        self.camera_process = threading.Thread(
            target=self.run_camera_window, 
            args=(device_id,),
            daemon=True
        )
        self.camera_process.start()
        
        # Update UI
        self.showing_camera = True
        self.camera_button.config(text="Stop Camera")
        self.record_button.config(state=tk.NORMAL)
        self.camera_status_label.config(text="Camera is running in a separate window.")
        
    def stop_camera(self):
        """Stop the camera and update UI"""
        # Signal camera thread to stop
        self.camera_should_run = False
        
        # Update UI
        self.showing_camera = False
        self.camera_button.config(text="Start Camera")
        self.record_button.config(state=tk.DISABLED)
        self.camera_status_label.config(text="Camera is stopped. Click 'Start Camera' to begin.")

        # Reset recording if active
        if self.is_recording:
            self.toggle_recording()
    
    def handle_camera_error(self, error_msg):
        """Handle camera errors consistently"""
        print(error_msg)
        messagebox.showerror("Camera Error", error_msg)
        self.reset_camera_ui()
    
    def run_camera_window(self, device_id):
        """Run camera in a separate window using direct OpenCV approach"""
        cap = None
        video_writer = None
        
        try:
            # Setup camera window
            window_name = "Camera Preview"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            
            # Open camera
            cap = cv2.VideoCapture(device_id)
            
            if not cap.isOpened():
                self.handle_camera_error(f"Could not open camera device {device_id}. Try another device ID.")
                return
                
            # Initialize camera
            self.setup_camera_and_ui(cap, window_name)
            
            # Main camera loop
            self.run_camera_loop(cap, window_name, video_writer)
            
        except Exception as e:
            self.handle_camera_error(f"Error in camera window: {str(e)}")
        finally:
            # Clean up resources
            self.cleanup_camera_resources(cap, video_writer, window_name)
            
    def setup_camera_and_ui(self, cap, window_name):
        """Set up camera and update UI with camera info"""
        # Get camera properties
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Setup window
        cv2.resizeWindow(window_name, int(width), int(height))
        
        # Update UI with camera info
        camera_info = f"Resolution: {width}x{height}, FPS: {fps}"
        print(f"Camera opened successfully: {camera_info}")
        self.root.after(0, lambda: self.camera_info_label.config(text=camera_info))
    
    def run_camera_loop(self, cap, window_name, video_writer=None):
        """Run the main camera loop for capturing and displaying frames"""
        while self.camera_should_run:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame")
                break
                
            # Store current frame
            self.current_frame = frame
            
            # Handle recording
            video_writer = self.handle_recording(cap, frame, video_writer)
            
            # Show frame
            cv2.imshow(window_name, frame)
            
            # Check for key press (q or ESC to quit)
            if self.check_exit_keys():
                break
                
        return video_writer
    
    def handle_recording(self, cap, frame, video_writer):
        """Handle video recording start/stop based on recording flag"""
        if self.is_recording and video_writer is None:
            # Start recording
            video_writer = self.start_new_recording(cap)
            
        if not self.is_recording and video_writer is not None:
            # Stop recording
            video_writer.release()
            video_writer = None
            print("Recording stopped")
            self.root.after(0, self.refresh_video_list)
            
        # Write frame if recording
        if self.is_recording and video_writer is not None:
            video_writer.write(frame)
            
        return video_writer
    
    def start_new_recording(self, cap):
        """Start a new video recording"""
        # Create filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(VIDEO_DIR, f"recording_{timestamp}.avi")
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create writer
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))
        print(f"Started recording to: {filename}")
        
        return video_writer
    
    def check_exit_keys(self):
        """Check for exit keys (q or ESC)"""
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 27 is ESC key
            print("Camera stopped by user")
            self.root.after(0, self.reset_camera_ui)
            return True
        return False
    
    def cleanup_camera_resources(self, cap, video_writer, window_name):
        """Clean up camera resources"""
        # Release video writer if active
        if video_writer is not None:
            video_writer.release()
            
        # Release camera
        if cap is not None and cap.isOpened():
            cap.release()
            
        # Close window
        try:
            cv2.destroyWindow(window_name)
        except:
            pass
            
        print("Camera resources cleaned up")
        
        # Reset UI in main thread
        self.root.after(0, self.reset_camera_ui)

    def reset_camera_ui(self):
        """Reset UI after camera has stopped"""
        self.showing_camera = False
        self.camera_button.config(text="Start Camera")
        self.record_button.config(state=tk.DISABLED)
        self.camera_status_label.config(text="Camera is stopped. Click 'Start Camera' to begin.")
        if self.is_recording:
            self.toggle_recording()
                
    def toggle_recording(self):
        """Toggle recording state"""
        if not self.showing_camera:
            return
            
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            self.record_button.config(text="Stop Recording")
            self.recording_label.config(text="Recording...")
        else:
            self.record_button.config(text="Start Recording")
            self.recording_label.config(text="")

    def refresh_video_list(self):
        """Refresh the list of recorded videos"""
        # Clear current list
        self.videos_listbox.delete(0, tk.END)

        # Get and display video files
        videos = self.get_available_videos()
        
        for video in sorted(videos, reverse=True):
            self.videos_listbox.insert(tk.END, video)
    
    def get_available_videos(self):
        """Get list of available video files"""
        if not os.path.exists(VIDEO_DIR):
            return []
            
        return [
            f for f in os.listdir(VIDEO_DIR) 
            if f.lower().endswith((".avi", ".mp4"))
        ]

    def delete_selected_video(self):
        """Delete the selected video file"""
        # Get selected video
        video_path = self.get_selected_video_path()
        if not video_path:
            return
            
        # Confirm deletion
        video_name = os.path.basename(video_path)
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete {video_name}?"):
            return
            
        # Delete the file
        try:
            os.remove(video_path)
            self.refresh_video_list()
            messagebox.showinfo("Success", "Video deleted successfully")
        except Exception as e:
            error_msg = f"Failed to delete video: {str(e)}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)

    def on_closing(self):
        """Handle application closing"""
        print("Closing application and cleaning up resources...")
        
        # Stop background threads
        self.stop_background_threads()
        
        # Release resources
        self.release_resources()
        
        # Destroy main window
        self.root.destroy()
    
    def stop_background_threads(self):
        """Stop all background threads"""
        # Stop weather checking
        self.weather_check_running = False
        
        # Stop camera
        self.camera_should_run = False
        
        # Reset recording
        self.is_recording = False
    
    def release_resources(self):
        """Release all resources"""
        # Release camera if exists
        if hasattr(self, 'camera') and self.camera:
            try:
                self.camera.release()
                print("Camera released")
            except:
                pass
        
        # Release video writer if exists
        if hasattr(self, 'video_writer') and self.video_writer:
            try:
                self.video_writer.release()
                print("Video writer released")
            except:
                pass
        
        # Close all OpenCV windows
        try:
            cv2.destroyAllWindows()
            print("All OpenCV windows closed")
        except:
            pass

    def play_selected_video(self):
        """Play the selected video in a separate window"""
        # Get selected video
        video_path = self.get_selected_video_path()
        if not video_path:
            return
            
        # Play video in a separate thread
        threading.Thread(
            target=self.play_video,
            args=(video_path,),
            daemon=True
        ).start()
    
    def get_selected_video_path(self):
        """Get the path of the selected video or show error"""
        selected = self.videos_listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "Please select a video to play")
            return None
            
        video_name = self.videos_listbox.get(selected[0])
        video_path = os.path.join(VIDEO_DIR, video_name)
        
        if not os.path.exists(video_path):
            messagebox.showerror("Error", f"Video file not found: {video_path}")
            return None
            
        return video_path
    
    def play_video(self, video_path):
        """Play a video file using OpenCV"""
        video_name = os.path.basename(video_path)
        window_name = f"Video Player - {video_name}"
        cap = None
        
        try:
            print(f"Playing video file: {video_path}")
            
            # Create window
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            
            # Open video file
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Failed to open video file: {video_path}")
                messagebox.showerror("Error", f"Could not open video file: {video_path}")
                return
                
            # Setup video playback
            self.setup_video_playback(cap, window_name)
            
            # Play video frames
            self.play_video_frames(cap, window_name)
                
        except Exception as e:
            print(f"Error playing video: {str(e)}")
            messagebox.showerror("Error", f"Error playing video: {str(e)}")
        finally:
            # Clean up resources
            self.cleanup_video_resources(cap, window_name)
    
    def setup_video_playback(self, cap, window_name):
        """Setup video playback parameters and window"""
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Use default FPS if invalid
        if fps <= 0:
            fps = 30
            
        # Set properties for playback
        self.video_fps = fps
        
        # Resize window to video dimensions
        cv2.resizeWindow(window_name, width, height)
        
        print(f"Video properties: {width}x{height}, {fps} FPS, {frame_count} frames")
    
    def play_video_frames(self, cap, window_name):
        """Play all frames from the video"""
        frames_played = 0
        
        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                break
                
            # Show frame
            frames_played += 1
            cv2.imshow(window_name, frame)
            
            # Calculate delay to maintain correct framerate
            delay = int(1000 / self.video_fps)
            
            # Check for exit keys
            key = cv2.waitKey(delay) & 0xFF
            if key == ord('q') or key == 27:  # q or ESC to quit
                break
                
        print(f"Finished playing video: {frames_played} frames")
    
    def cleanup_video_resources(self, cap, window_name):
        """Clean up resources after video playback"""
        try:
            if cap is not None and cap.isOpened():
                cap.release()
                
            cv2.destroyWindow(window_name)
        except Exception as e:
            print(f"Error cleaning up video resources: {str(e)}")
            cv2.destroyAllWindows()

    def detect_cameras(self):
        """Detect available cameras on the system"""
        # Clear previous list
        self.cameras_listbox.delete(0, tk.END)
        
        # Create progress window
        progress_win = self.create_camera_detection_progress_window()
        
        # Start detection in background thread
        threading.Thread(
            target=self.scan_cameras,
            args=(progress_win,),
            daemon=True
        ).start()
    
    def create_camera_detection_progress_window(self):
        """Create a progress window for camera detection"""
        progress_win = tk.Toplevel(self.root)
        progress_win.title("Detecting Cameras")
        progress_win.geometry("300x100")
        progress_win.transient(self.root)
        progress_win.grab_set()
        
        ttk.Label(progress_win, text="Scanning for connected cameras...").pack(pady=10)
        progress_bar = ttk.Progressbar(progress_win, mode="indeterminate", length=200)
        progress_bar.pack(pady=10)
        progress_bar.start()
        
        return progress_win
    
    def scan_cameras(self, progress_win):
        """Scan for connected cameras and update the UI with results"""
        available_cameras = []
        
        # Try first 5 camera indices
        for i in range(5):
            # Try both methods to detect cameras
            result = self.try_camera_with_method(i, cv2.CAP_ANY)
            if not result:
                result = self.try_camera_with_method(i, cv2.CAP_DSHOW)
            
            if result:
                available_cameras.append(result)
        
        # Update UI from main thread
        self.root.after(0, lambda: self.update_camera_list(available_cameras, progress_win))
    
    def try_camera_with_method(self, index, api_preference=cv2.CAP_ANY):
        """Try to open and test a camera with specific API preference"""
        try:
            print(f"Checking camera index {index} with API preference {api_preference}")
            cap = cv2.VideoCapture(index, api_preference)
            
            if not cap.isOpened():
                if cap.isOpened():
                    cap.release()
                return None
                
            # Try to read a frame
            ret, frame = cap.read()
            if not ret or frame is None or frame.size == 0:
                cap.release()
                return None
                
            # Get camera properties
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Create camera description
            description = f"Camera {index}: {width}x{height}, {fps} FPS"
            if api_preference == cv2.CAP_DSHOW:
                description += " (DirectShow)"
            
            # Release camera
            cap.release()
            
            return (index, description)
            
        except Exception as e:
            print(f"Error checking camera {index}: {str(e)}")
            return None
    
    def update_camera_list(self, available_cameras, progress_win):
        """Update the camera list UI with detection results"""
        # Close progress window
        progress_win.grab_release()
        progress_win.destroy()
        
        # Update listbox
        if available_cameras:
            for idx, desc in available_cameras:
                self.cameras_listbox.insert(tk.END, desc)
            messagebox.showinfo("Cameras Detected", f"Found {len(available_cameras)} available cameras.")
        else:
            self.cameras_listbox.insert(tk.END, "No cameras detected!")
            messagebox.showwarning("No Cameras", 
                "No cameras were detected on your system. Check your connections and drivers.")
    
    def select_camera_from_list(self, event):
        """Handle camera selection from the listbox"""
        selected = self.cameras_listbox.curselection()
        if not selected:
            return
            
        # Extract camera index from the description
        camera_desc = self.cameras_listbox.get(selected[0])
        camera_idx = camera_desc.split(":")[0].replace("Camera ", "").strip()
        
        # Update entry field
        self.camera_device.delete(0, tk.END)
        self.camera_device.insert(0, camera_idx)
        
        # Show confirmation
        messagebox.showinfo("Camera Selected", f"Selected {camera_desc}")


if __name__ == "__main__":
    # Create and run application
    root = tk.Tk()
    app = WeatherCameraApp(root)
    root.mainloop()
