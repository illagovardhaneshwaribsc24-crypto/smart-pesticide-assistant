from PIL import Image


def load_image(uploaded_file):
    """
    Load an image from uploaded file and preprocess it for ML models.
    Converts to RGB and resizes to 224x224.
    """
    image = Image.open(uploaded_file).convert("RGB")
    image = image.resize((224, 224))
    return image