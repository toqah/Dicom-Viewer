import tkinter as tk
from tkinter import filedialog, messagebox
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DicomViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DICOM Viewer")
        self.file_path = None
        self.dicom_data = None
        self.image_data = None
        
        self.fig = plt.figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        
        self.create_menu()
        self.create_toolbar()
        
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open DICOM", command=self.browse_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Axial", command=self.axial_view)
        view_menu.add_command(label="Coronal", command=self.coronal_view)
        view_menu.add_command(label="Sagittal", command=self.sagittal_view)
        menu_bar.add_cascade(label="View", menu=view_menu)
        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="DICOM Information", command=self.show_dicom_info)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)
        
    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        
        browse_button = tk.Button(toolbar, text="Browse", command=self.browse_file)
        browse_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        segment_button = tk.Button(toolbar, text="Segment Bones", command=self.segment_bones)
        segment_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("DICOM Files", "*.dcm")])
        if file_path:
            self.file_path = file_path
            self.load_dicom_data()
            self.axial_view()
        
    def load_dicom_data(self):
        self.dicom_data = pydicom.dcmread(self.file_path)
        self.image_data = self.dicom_data.pixel_array
        
    def axial_view(self):
        if self.dicom_data is None:
            return
        
        self.fig.clear()
        plt.imshow(self.image_data, cmap=plt.cm.hot, aspect='auto')
        plt.title('Axial View')
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.colorbar()
        self.canvas.draw()
        
    def coronal_view(self):
        if self.dicom_data is None:
            return
        
        self.fig.clear()
        plt.imshow(self.image_data.transpose(), cmap=plt.cm.hot, aspect='auto')
        plt.title('Coronal View')
        plt.xlabel('Column')
        plt.ylabel('Slice')
        plt.colorbar()
        self.canvas.draw()
        
    def sagittal_view(self):
        if self.dicom_data is None:
            return
        
        self.fig.clear()
        plt.imshow(np.rot90(self.image_data), cmap=plt.cm.hot, aspect='auto')
        plt.title('Sagittal View')
        plt.xlabel('Slice')
        plt.ylabel('Row')
        plt.colorbar()
        self.canvas.draw()
        
    def show_dicom_info(self):
        if self.dicom_data is None:
            return
        
        info = f"Patient Name: {self.dicom_data.PatientName}\n" \
               f"Patient ID: {self.dicom_data.PatientID}\n" \
               f"Modality: {self.dicom_data.Modality}\n" \
               f"Study Description: {self.dicom_data.StudyDescription}\n" \
               f"Study Date: {self.dicom_data.StudyDate}\n" \
               f"Study Time: {self.dicom_data.StudyTime}\n" \
               f"Manufacturer: {self.dicom_data.Manufacturer}"
        
        messagebox.showinfo("DICOM Information", info)
        
    def segment_bones(self):
        if self.dicom_data is None:
            return
        
        threshold = 400
        segmented_image = np.where(self.image_data >= threshold, 1, 0)
        
        plt.figure()
        plt.imshow(segmented_image, cmap=plt.cm.hot, aspect='auto')
        plt.title('Segmented Bones')
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.colorbar()
        plt.show()
        
    def run(self):
        self.root.mainloop()

# Create the Tkinter window
window = tk.Tk()

# Create the DicomViewerApp instance
app = DicomViewerApp(window)

# Run the Tkinter event loop
app.run()
