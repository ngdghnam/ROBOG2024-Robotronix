import argparse
import pickle
from collections import Counter
from pathlib import Path

import face_recognition
from PIL import Image, ImageDraw

Path("./Functions/FaceRecognition/training").mkdir(exist_ok=True)
Path("./Functions/FaceRecognition/output").mkdir(exist_ok=True)
Path("./Functions/FaceRecognition/validation").mkdir(exist_ok=True)

DEFAULT_ENCODING_PATH = Path("./Functions/FaceRecognition/output/encodings.pkl")
BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"

parser = argparse.ArgumentParser(description="Recognize faces in an image")
parser.add_argument("--train", action="store_true", help="Train on input data")
parser.add_argument(
    "--validate", action="store_true", help="Validate trained model"
)
parser.add_argument(
    "--test", action="store_true", help="Test the model with an unknown image"
)
parser.add_argument(
    "-m",
    action="store",
    default="hog",
    choices=["hog","cnn"],
    help="Which model to use for training: hog (CPU), cnn (GPU)",
)
parser.add_argument(
    "-f", action="store", help="Path to an image with an unknown face"
)
args = parser.parse_args()

def encode_known_faces(
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODING_PATH
) -> None:
    names = []
    encodings = []
    for filepath in Path("./Functions/FaceRecognition/training").glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)
        
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)

#chạy lệnh này trước để build model (ông tạo folder trong training như mẫu rồi thêm nhiều ảnh vào rồi mới chạy lệnh này nha)
#encode_known_faces()
def recognize_faces(
    image_location: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODING_PATH,
) -> str:
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)
    
    input_image = face_recognition.load_image_file(image_location)
    
    input_face_locations = face_recognition.face_locations(input_image, model=model)
    input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)
    
    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)
    
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        #print(name, bounding_box)
        _display_face(draw, bounding_box, name)
    
    del draw
    pillow_image.show()
    return str(name)

def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(
        name 
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]

def _display_face(draw, bounding_box, name):
    top, right, bottom, left = bounding_box
    draw.rectangle(((left,top), (right,bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill = "blue",
        outline = "blue",
    )
    draw.text(
        (text_left,text_top),
        name,
        fill="white",
    )
#chạy lệnh này để muốn test nhanh hình ảnh bất kỳ (nên cmt dòng lệnh encode_known_faces() ở trên để tránh mất thời gian nếu như ông đã build model trước đó)
#recognize_faces("unknown1.jpg")

def validate(model: str = "hog"):
    for filepath in Path("./Functions/FaceRecognition/validation").rglob("*"):
        if filepath.is_file():
            recognize_faces(
                image_location=str(filepath.absolute()), model=model
            )
#validate()

if __name__ == "__main__":
    if args.train:
        encode_known_faces(model=args.m)
    if args.validate:
        validate(model=args.m)
    if args.test:
        recognize_faces(image_location=args.f, model=args.m)
    validate()
#Có thể chạy trong terminal (ông đọc trên phần parser): python detector.py --test -f <image_dir> 
