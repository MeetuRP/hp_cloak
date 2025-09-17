# 🪄 Real-time "Harry Potter Invisibility Cloak" using OpenCV

This Python project uses computer vision techniques with OpenCV to create a real-time "invisibility cloak" effect, inspired by the one from the Harry Potter series. It intelligently replaces a specific color in a webcam feed with a static background image, making objects of that color appear invisible.

The application features an advanced interactive calibration system, allowing the user to fine-tune the color detection for high accuracy in any lighting condition.



---

## ## Features

-   **Real-Time Video Processing:** Applies the invisibility effect to a live webcam feed.
-   **Interactive Color Calibration:** A dedicated "HSV Calibration" window with trackbars allows you to precisely select the cloak's color on the fly.
-   **Advanced Masking:** Uses morphological transformations and contour detection to create a clean, stable mask of the cloak, ignoring small color noises.
-   **Edge Blending (Feathering):** Implements alpha blending with a blurred mask to create soft, seamless edges for a truly "magical" and realistic effect.
-   **Static Background Capture:** Captures and stores the background scene to project onto the cloak.
-   **Keyboard Controls:** Easily recapture the background or quit the application.
-   **Full-Screen Mode:** The main window opens in full-screen for an immersive experience.

---

## ## Requirements

-   Python 3.x
-   OpenCV
-   NumPy

---

## ## Installation

1.  Clone or download this repository.
2.  Install the required Python libraries using pip:

    ```bash
    pip install opencv-python numpy
    ```

---

## ## How to Use

Follow these steps to get the best results:

1.  **Set Up Your Scene:** Place your webcam in a stable position. Ensure you have **good, consistent lighting** in your room. Avoid shadows and changing light sources.

2.  **Run the Script:** Open your terminal or command prompt, navigate to the project directory, and run the script:

    ```bash
    python cloak.py
    ```

3.  **Capture the Background:** The script will first capture the background. When you see the console prompt "Capturing background...", **step completely out of the camera's view**. Stay out of the frame for a few seconds until you see "Background captured".

4.  **Calibrate the Cloak Color:**
    -   Step back into the frame holding your colored cloth (the script is pre-set for **red**, but you can adapt it to any color).
    -   Three windows will appear: "Invisibility Cloak", "Cloak Mask (debug)", and "HSV Calibration".
    -   Use the sliders in the **"HSV Calibration"** window to perfectly isolate the color of your cloak.
    -   **Your Goal:** Adjust the `Lower` and `Upper` HSV sliders until the **"Cloak Mask (debug)"** window shows your cloak as a solid **white shape** against a completely **black background**.

5.  **Enjoy the Magic!** Once calibrated, the main "Invisibility Cloak" window will display the final, seamless effect.

---

## ## Keyboard Controls

While the application is running:

-   **`b` key**: Recaptures the background. Use this if the lighting changes or if the initial background was not captured correctly.
-   **`ESC` key**: Quits the application and closes all windows.

---

## ## How It Works

The magic is achieved through a sequence of computer vision techniques:

1.  **Background Capture:** The script first records and stores a static image of the background scenery.
2.  **Color Thresholding:** In each new frame, the image is converted to the HSV (Hue, Saturation, Value) color space, which is ideal for color detection. The user-defined range from the trackbars is used to create a binary mask, isolating pixels that match the cloak's color.
3.  **Mask Refinement:** The initial mask is cleaned up using **morphological operations** (`MORPH_OPEN` and `MORPH_CLOSE`) to remove noise and fill holes. The script then finds the **largest contour** in the mask, assuming it's the cloak, which eliminates any other small, incorrectly detected color patches.
4.  **Edge Blending:** The clean mask's edges are blurred using a **Gaussian Blur**. This "feathering" is the key to the smooth effect.
5.  **Alpha Blending:** The final image is created by combining the static background and the current frame. The blurred mask acts as an alpha channel, determining the transparency of each pixel. Where the mask is white, the background is shown; where it's black, the current frame is shown. The gray, blurry edges create a seamless, semi-transparent transition.

---
created by Meet Parmar
connect with me: [LinkedIn](https://www.linkedin.com/in/meet-parmar-28jan2005/)
