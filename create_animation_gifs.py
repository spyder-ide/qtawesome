"""
Script to create GIFs from qtawesome animation examples.

This script captures the example_animations.py and example_combined_animations.py
windows as GIF files for documentation purposes.
"""

import sys
import time
from pathlib import Path

from qtpy import QtWidgets, QtCore, QtGui

try:
    from PIL import Image
except ImportError:
    print("PIL/Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


class AnimationRecorder:
    """Records animation window to a series of images and saves as GIF."""

    def __init__(self, window, output_path, duration=5000, fps=20):
        """
        Parameters
        ----------
        window : QWidget
            The window to record
        output_path : str or Path
            Path to save the GIF file
        duration : int
            How long to record in milliseconds
        fps : int
            Frames per second for the recording
        """
        self.window = window
        self.output_path = Path(output_path)
        self.duration = duration
        self.fps = fps
        self.frames = []
        self.timer = QtCore.QTimer()
        self.start_time = None

    def start_recording(self):
        """Start recording the window."""
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

        # Wait a bit for the window to be fully rendered and animations to start
        QtCore.QTimer.singleShot(800, self._begin_capture)

    def _begin_capture(self):
        """Begin capturing frames."""
        self.start_time = time.time()
        self.timer.timeout.connect(self._capture_frame)
        self.timer.start(1000 // self.fps)

    def _capture_frame(self):
        """Capture a single frame."""
        elapsed = int((time.time() - self.start_time) * 1000)

        if elapsed >= self.duration:
            self.timer.stop()
            self._save_gif()
            self.window.close()
            QtWidgets.QApplication.quit()
            return

        # Capture the window as an image
        pixmap = self.window.grab()

        # Convert QPixmap to PIL Image
        qimage = pixmap.toImage()
        buffer = qimage.bits().asstring(qimage.sizeInBytes())
        img = Image.frombytes(
            "RGBA",
            (qimage.width(), qimage.height()),
            buffer,
            "raw",
            "BGRA"
        )

        # Convert RGBA to RGB (GIF doesn't support transparency well)
        rgb_img = Image.new("RGB", img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3])

        self.frames.append(rgb_img)

    def _save_gif(self):
        """Save captured frames as GIF."""
        if not self.frames:
            print(f"No frames captured for {self.output_path}")
            return

        print(f"Saving {len(self.frames)} frames to {self.output_path}")

        # Save as GIF
        self.frames[0].save(
            self.output_path,
            save_all=True,
            append_images=self.frames[1:],
            duration=1000 // self.fps,
            loop=0,
            optimize=True
        )
        print(f"GIF saved: {self.output_path}")


def record_example(example_module, output_filename, duration, fps):
    """
    Record an example module's window as a GIF.

    Parameters
    ----------
    example_module : str
        Name of the example module (e.g., 'example_animations')
    output_filename : str
        Name of the output GIF file
    duration : int
        Recording duration in milliseconds
    fps : int
        Frames per second
    """
    # Import the example module
    if example_module == 'example_animations':
        from example_animations import AnimationTestWindow as WindowClass
    elif example_module == 'example_combined_animations':
        from example_combined_animations import NewAnimationTestWindow as WindowClass
    else:
        raise ValueError(f"Unknown example module: {example_module}")

    # Create the window
    window = WindowClass()

    return window, output_filename


def main():
    """Main function to create all GIFs."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Create GIF animations from qtawesome example scripts'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='',
        help='Output directory for GIF files'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=5000,
        help='Duration of each GIF in milliseconds (default: 5000)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=20,
        help='Frames per second (default: 20)'
    )
    parser.add_argument(
        '--examples',
        nargs='+',
        choices=['basic', 'combined', 'all'],
        default=['all'],
        help='Which examples to generate: basic (example_animations), combined (example_combined_animations), or all'
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine which examples to run
    examples = []
    if 'all' in args.examples or 'basic' in args.examples:
        examples.append(('example_animations', 'qtawesome-animations-basic.gif'))
    if 'all' in args.examples or 'combined' in args.examples:
        examples.append(('example_combined_animations', 'qtawesome-animations-combined.gif'))

    print(f"Creating {len(examples)} animation GIFs...")
    print(f"Output directory: {output_dir}")
    print(f"Duration: {args.duration}ms, FPS: {args.fps}")
    print()

    # Create each example
    for example_module, output_filename in examples:
        print(f"Creating {output_filename} from {example_module}.py...")

        # Create new QApplication for each example
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)

        try:
            # Create the example window
            window, filename = record_example(
                example_module,
                output_filename,
                args.duration,
                args.fps
            )
            output_path = output_dir / filename

            # Create recorder and start
            recorder = AnimationRecorder(
                window,
                output_path,
                duration=args.duration,
                fps=args.fps
            )
            recorder.start_recording()

            # Run the application
            app.exec_()

            print(f"Completed {output_filename}\n")

        except Exception as e:
            print(f"Error creating {output_filename}: {e}\n")
            continue

    print("All GIFs created successfully!")


if __name__ == '__main__':
    main()
