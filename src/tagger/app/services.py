import io

import numpy as np
from app.logging import logger
from onnxruntime import InferenceSession
from PIL import Image


class TaggingService:
    def __init__(self, model_session: InferenceSession, tags_list: list[str]):
        self._model_session = model_session
        self._tags_list = tags_list

    def predict_tags(
        self, image_buff: bytes, score_threshold: float = 0.5
    ) -> list[str]:
        logger.info("opening image")
        image = Image.open(io.BytesIO(image_buff))
        s = 512
        w, h = image.size
        h, w = (s, int(s * w / h)) if h > w else (int(s * h / w), s)
        ph, pw = s - h, s - w
        image = image.resize((w, h))

        logger.info("converting image")
        image_array = np.array(image).astype(np.float32) / 255
        pad_width = ((ph // 2, ph - ph // 2), (pw // 2, pw - pw // 2), (0, 0))
        image_array = np.pad(image_array, pad_width, mode="edge")
        image_array = image_array[np.newaxis, :]

        logger.info("predicting probs")
        probs = self._model_session.run(None, {"input_1": image_array})[0][0]
        probs = probs.astype(np.float32)

        logger.info("extracting tags")
        extracted_tags = []
        for prob, label in zip(probs.tolist(), self._tags_list):
            if prob < score_threshold:
                continue
            label = label.replace(":", "_")
            extracted_tags.append(label)

        return extracted_tags
