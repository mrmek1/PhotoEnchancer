# Photo Enhancer

A simple, open-source photo processing application that automatically enhances images in bulk by adjusting brightness, contrast, and saturation.

<div class="image-comparison" style="position: relative; width: 100%; max-width: 600px; margin: 20px auto;">
    <img src="screenshots/Before.jpg" style="width: 100%;" alt="Before enhancement">
    <div class="comparison-overlay" style="position: absolute; top: 0; left: 0; width: 50%; height: 100%; overflow: hidden;">
        <img src="screenshots/After.jpg" style="width: 200%;" alt="After enhancement">
    </div>
    <input type="range" class="comparison-slider" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; -webkit-appearance: none; background: none; cursor: pointer; margin: 0;" min="0" max="100" value="50">
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.comparison-slider');
    const overlay = document.querySelector('.comparison-overlay');
    
    slider.addEventListener('input', function() {
        overlay.style.width = this.value + '%';
    });
});
</script>

## Features

- Batch process multiple images at once
- Adjustable enhancement settings:
  - Brightness (0.5 - 2.0)
  - Contrast (0.5 - 2.0)
  - Saturation (0.5 - 2.0)
- Settings are automatically saved
- Simple and intuitive interface
- Progress tracking
- Cancel processing at any time

## Screenshots

<div align="center">
    <img src="screenshots/interface.png" alt="Main application window" width="600"/>
</div>

