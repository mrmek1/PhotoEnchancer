import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from image_processor import ImageEnhancer
import os
from PIL import Image, ImageTk
import threading
import json
from io import BytesIO

class ImageProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Enhancer")
        self.root.geometry("800x700")
        
        self.load_settings()
        
        self.colors = {
            'bg': '#2C3E50',
            'fg': '#ECF0F1',
            'accent': '#3498DB',
            'success': '#2ECC71',
            'warning': '#E74C3C',
            'slider': '#3498DB'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.style = ttk.Style()
        self.style.configure('Custom.TButton', 
                           padding=10, 
                           font=('Helvetica', 10, 'bold'),
                           background=self.colors['accent'])
        
        self.style.configure('Custom.TFrame', 
                           background=self.colors['bg'])
        
        self.style.configure('Custom.TLabelframe', 
                           padding=15,
                           font=('Helvetica', 11, 'bold'),
                           background=self.colors['bg'],
                           foreground=self.colors['fg'])
        
        self.style.configure('Title.TLabel', 
                           font=('Helvetica', 24, 'bold'),
                           foreground=self.colors['accent'],
                           background=self.colors['bg'])
        
        self.style.configure('Header.TLabel', 
                           font=('Helvetica', 12),
                           foreground=self.colors['fg'],
                           background=self.colors['bg'])
        
        self.style.configure("Custom.Horizontal.TScale",
                           background=self.colors['bg'],
                           troughcolor=self.colors['accent'],
                           sliderwidth=15,
                           sliderlength=20)
        
        self.main_frame = ttk.Frame(root, style='Custom.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.create_header()
        self.create_settings_section()
        self.create_folder_selection()
        self.create_progress_section()
        self.create_footer()
        self.create_exit_button()
        self.center_window()
        
        self.cancel_flag = False

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.brightness_value = settings.get('brightness', 1.27)
                self.contrast_value = settings.get('contrast', 1.1)
                self.saturation_value = settings.get('saturation', 1.05)
        except:
            self.brightness_value = 1.27
            self.contrast_value = 1.1
            self.saturation_value = 1.05

    def save_settings(self):
        settings = {
            'brightness': self.brightness_var.get(),
            'contrast': self.contrast_var.get(),
            'saturation': self.saturation_var.get()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def create_header(self):
        header_frame = ttk.Frame(self.root, style='Custom.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=(20,10))
        
        ttk.Label(header_frame, text="Photo Enhancer", style='Title.TLabel').pack(pady=5)
        ttk.Label(header_frame, text="Batch Image Processing Tool", style='Header.TLabel').pack()

    def create_settings_section(self):
        settings_frame = ttk.LabelFrame(self.main_frame, 
                                      text="Enhancement Settings", 
                                      style='Custom.TLabelframe')
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        def on_slider_release(var, value_label):
            value_label.configure(text=f"{var.get():.2f}")
            self.save_settings()

        self.create_slider(settings_frame, 
                         "Brightness", 
                         self.brightness_value,
                         on_slider_release)
        
        self.create_slider(settings_frame, 
                         "Contrast", 
                         self.contrast_value,
                         on_slider_release)
        
        self.create_slider(settings_frame, 
                         "Saturation", 
                         self.saturation_value,
                         on_slider_release)

        reset_frame = ttk.Frame(settings_frame, style='Custom.TFrame')
        reset_frame.pack(fill=tk.X, padx=5, pady=10)
        
        reset_btn = ttk.Button(reset_frame, 
                             text="Reset to Defaults",
                             command=self.reset_settings,
                             style='Custom.TButton')
        reset_btn.pack(side=tk.RIGHT)

    def create_slider(self, parent, label_text, default_value, callback):
        frame = ttk.Frame(parent, style='Custom.TFrame')
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, 
                 text=f"{label_text}:", 
                 style='Header.TLabel',
                 width=10).pack(side=tk.LEFT, padx=5)
        
        var = tk.DoubleVar(value=default_value)
        setattr(self, f"{label_text.lower()}_var", var)
        
        value_label = ttk.Label(frame, 
                              text=f"{default_value:.2f}",
                              style='Header.TLabel',
                              width=5)
        value_label.pack(side=tk.RIGHT, padx=5)
        
        def on_slider_change(event=None):
            value_label.configure(text=f"{var.get():.2f}")
        
        def on_slider_release(event=None):
            callback(var, value_label)
        
        slider = ttk.Scale(frame,
                         from_=0.5,
                         to=2.0,
                         variable=var,
                         orient=tk.HORIZONTAL,
                         style="Custom.Horizontal.TScale")
        
        slider.bind("<Motion>", on_slider_change)
        slider.bind("<ButtonRelease-1>", on_slider_release)
        var.trace('w', lambda *args: on_slider_change())
        
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        return slider

    def reset_settings(self):
        self.brightness_var.set(1.27)
        self.contrast_var.set(1.1)
        self.saturation_var.set(1.05)
        self.save_settings()

    def create_folder_selection(self):
        folder_frame = ttk.LabelFrame(self.main_frame, text="Folder Selection", style='Custom.TLabelframe')
        folder_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_frame = ttk.Frame(folder_frame, style='Custom.TFrame')
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Input Folder:", style='Header.TLabel').pack(side=tk.LEFT, padx=5)
        self.input_folder = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_folder, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Browse", command=self.select_input_folder, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        
        output_frame = ttk.Frame(folder_frame, style='Custom.TFrame')
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(output_frame, text="Output Folder:", style='Header.TLabel').pack(side=tk.LEFT, padx=5)
        self.output_folder = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_folder, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=self.select_output_folder, style='Custom.TButton').pack(side=tk.LEFT, padx=5)

    def create_progress_section(self):
        progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", style='Custom.TLabelframe')
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.progress.pack(pady=10, fill=tk.X, padx=10)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var, style='Header.TLabel')
        self.status_label.pack(pady=5)
        
        button_frame = ttk.Frame(progress_frame, style='Custom.TFrame')
        button_frame.pack(pady=10)
        
        self.process_button = ttk.Button(button_frame, text="Start Processing", command=self.start_processing, style='Custom.TButton')
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_processing, style='Custom.TButton')
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def create_footer(self):
        footer_frame = ttk.Frame(self.root, style='Custom.TFrame')
        footer_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(footer_frame, text="Open Source Photo Enhancement Tool", style='Header.TLabel').pack()

    def create_exit_button(self):
        exit_frame = ttk.Frame(self.root, style='Custom.TFrame')
        exit_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Button(exit_frame, text="Exit", command=self.root.quit, style='Custom.TButton').pack(side=tk.RIGHT)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder", initialdir=os.path.expanduser("~"))
        if folder:
            self.input_folder.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder", initialdir=os.path.expanduser("~"))
        if folder:
            self.output_folder.set(folder)

    def validate_inputs(self):
        if not self.input_folder.get():
            messagebox.showerror("Error", "Please select input folder!")
            return False
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select output folder!")
            return False
        if not os.path.exists(self.input_folder.get()):
            messagebox.showerror("Error", "Input folder not found!")
            return False
        return True

    def cancel_processing(self):
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel the process?"):
            self.cancel_flag = True
            self.status_var.set("Canceling process...")

    def start_processing(self):
        if not self.validate_inputs():
            return
        
        self.cancel_flag = False
        os.makedirs(self.output_folder.get(), exist_ok=True)
        self.process_button['state'] = 'disabled'
        self.progress['value'] = 0
        
        thread = threading.Thread(target=self.process_images)
        thread.start()

    def process_images(self):
        try:
            enhancer = ImageEnhancer()
            # Update enhancer settings from GUI and save them
            enhancer.brightness_factor = self.brightness_var.get()
            enhancer.contrast_factor = self.contrast_var.get()
            enhancer.saturation_factor = self.saturation_var.get()
            self.save_settings()
            
            image_files = [f for f in os.listdir(self.input_folder.get())
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            total_files = len(image_files)
            
            if total_files == 0:
                messagebox.showwarning("Warning", "No images found to process!")
                return
            
            processed_count = 0
            for i, filename in enumerate(image_files):
                if self.cancel_flag:
                    break
                
                input_path = os.path.join(self.input_folder.get(), filename)
                output_path = os.path.join(self.output_folder.get(), f"enhanced_{filename}")
                
                self.status_var.set(f"Processing: {filename}")
                
                if enhancer.process_image(input_path, output_path):
                    processed_count += 1
                
                progress = (i + 1) / total_files * 100
                self.progress['value'] = progress
                self.root.update_idletasks()
            
            if self.cancel_flag:
                self.status_var.set("Process canceled")
                messagebox.showinfo("Canceled", "Process was canceled by user.")
            else:
                self.status_var.set("Process completed!")
                messagebox.showinfo("Success", f"{processed_count} images processed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.process_button['state'] = 'normal'
            self.cancel_flag = False

def main():
    root = tk.Tk()
    app = ImageProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 