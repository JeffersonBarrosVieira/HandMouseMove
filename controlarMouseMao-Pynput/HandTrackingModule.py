import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detecConfidence=0.5, trackingConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detecConfidence = detecConfidence
        self.trackingConf = trackingConf

        self.mpHands = mp.solutions.mediapipe.python.solutions.hands
        self.mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands,
                                        self.detecConfidence,
                                        self.trackingConf)

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []

        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), lm.z
                # print(id, cx, cy)
                lmList.append([id, cx, cy, cz])

                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)

        return lmList
        # 20,19,18,17 -> Dedo midinho
        # 16,15,14,13 -> Dedo anelar
        # 12,11,10,9 -> Dedo do meio
        # 8,7,6,5 -> Dedo do indicador
        # 4,3,2,1 -> Dedo polegar




def main():
    cap = cv2.VideoCapture(0)  # canal 0

    pTime = 0
    cTime = 0

    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[8])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
