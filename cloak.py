import cv2
import numpy as np
import time

# --- Function to do nothing (placeholder for trackbar) ---
def do_nothing(x):
    pass

# --- Create a window for the HSV trackbars ---
cv2.namedWindow("HSV Calibration")
cv2.createTrackbar("Lower H", "HSV Calibration", 0, 179, do_nothing)
cv2.createTrackbar("Lower S", "HSV Calibration", 120, 255, do_nothing)
cv2.createTrackbar("Lower V", "HSV Calibration", 70, 255, do_nothing)
cv2.createTrackbar("Upper H", "HSV Calibration", 10, 179, do_nothing)
cv2.createTrackbar("Upper S", "HSV Calibration", 255, 255, do_nothing)
cv2.createTrackbar("Upper V", "HSV Calibration", 255, 255, do_nothing)

# --- Webcam Setup ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not access the camera. Try using index 1 or 2.")
    exit()

# --- Set the main window to full screen ---
cv2.namedWindow("🪄 Invisibility Cloak", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("🪄 Invisibility Cloak", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


print("Waiting for camera to warm up...")
time.sleep(3) # Increased wait time for camera to stabilize

# --- Capture a stable background ---
print("📸 Capturing background... please step out of the frame.")
bg = None
for _ in range(90):
    ret, bg = cap.read()
    if ret:
        bg = cv2.flip(bg, 1)
print("✅ Background captured")


# --- Main Loop ---
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # --- Get HSV values from trackbars ---
    l_h = cv2.getTrackbarPos("Lower H", "HSV Calibration")
    l_s = cv2.getTrackbarPos("Lower S", "HSV Calibration")
    l_v = cv2.getTrackbarPos("Lower V", "HSV Calibration")
    u_h = cv2.getTrackbarPos("Upper H", "HSV Calibration")
    u_s = cv2.getTrackbarPos("Upper S", "HSV Calibration")
    u_v = cv2.getTrackbarPos("Upper V", "HSV Calibration")

    # --- Color Detection ---
    # Using MedianBlur is often better for removing salt-and-pepper noise
    blurred_frame = cv2.medianBlur(frame, 5)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper HSV ranges based on trackbar values
    lower_hsv = np.array([l_h, l_s, l_v])
    upper_hsv = np.array([u_h, u_s, u_v])
    
    # Handle red's wrap-around case in the HSV color space
    if l_h > u_h:
        lower_red1 = np.array([0, l_s, l_v])
        upper_red1 = np.array([u_h, u_s, u_v])
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        lower_red2 = np.array([l_h, l_s, l_v])
        upper_red2 = np.array([179, u_s, u_v])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        initial_mask = mask1 + mask2
    else:
        initial_mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # --- Mask Refinement ---
    kernel = np.ones((7, 7), np.uint8)
    initial_mask = cv2.morphologyEx(initial_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    initial_mask = cv2.morphologyEx(initial_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # --- Find Largest Contour ---
    contours, _ = cv2.findContours(initial_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(initial_mask)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 500:
            cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)

    # --- MAJOR IMPROVEMENT: Edge Blending (Feathering) ---
    # This is the key to the "magical" effect. We blur the mask to create soft edges.
    # The kernel size must be an odd number. A larger number means a softer edge.
    mask = cv2.GaussianBlur(mask, (15, 15), 0)

    # --- Alpha Blending for Seamless Combination ---
    # Convert mask to a 32-BIT float and normalize to range [0, 1] for blending
    mask_float = mask.astype('float32') / 255.0
    # Create an inverse mask for the foreground
    mask_inv_float = 1.0 - mask_float

    # Expand masks to 3 channels to multiply with color images
    mask_float = cv2.cvtColor(mask_float, cv2.COLOR_GRAY2BGR)
    mask_inv_float = cv2.cvtColor(mask_inv_float, cv2.COLOR_GRAY2BGR)

    # Convert frame and background to float for multiplication
    frame_float = frame.astype('float32')
    bg_float = bg.astype('float32')

    # Perform the alpha blending
    cloak_area = cv2.multiply(mask_float, bg_float)
    non_cloak_area = cv2.multiply(mask_inv_float, frame_float)

    # Combine and convert back to the original 8-bit format
    final_output = cv2.add(cloak_area, non_cloak_area).astype(np.uint8)

    # --- Display On-Screen Instructions ---
    cv2.putText(final_output, "Press 'b' to Recapture Background", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(final_output, "Press 'ESC' to Quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)

    # --- Show Windows ---
    cv2.imshow("🪄 Invisibility Cloak", final_output)
    cv2.imshow("🎭 Cloak Mask (debug)", mask) # This now shows the soft-edged mask

    # --- Keyboard Controls ---
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif key == ord('b'):
        print("♻️ Re-capturing background...")
        for _ in range(90):
            ret, bg = cap.read()
            if ret:
                bg = cv2.flip(bg, 1)
        print("✅ Background updated")

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()
