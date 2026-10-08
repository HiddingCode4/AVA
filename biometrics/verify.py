"""Experimental local face and speaker matching. Never a security boundary."""
import sys,json,base64,io
from pathlib import Path
import numpy as np
import cv2

def main(d):
    folder=Path(d['folder']);folder.mkdir(parents=True,exist_ok=True)
    action=d['action']
    if action.endswith('face'):
        raw=base64.b64decode(d['image'].split(',',1)[1]);im=cv2.imdecode(np.frombuffer(raw,np.uint8),cv2.IMREAD_GRAYSCALE)
        if im is None:raise ValueError('Image invalide')
        cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        faces=cascade.detectMultiScale(im,1.15,5,minSize=(90,90))
        if len(faces)!=1:return {'match':False,'message':'Un seul visage bien éclairé doit être visible'}
        x,y,w,h=faces[0];crop=cv2.resize(im[y:y+h,x:x+w],(160,160));crop=cv2.equalizeHist(crop)
        target=folder/'face.yml';model=cv2.face.LBPHFaceRecognizer_create()
        if action=='enroll_face':
            images=[crop,cv2.convertScaleAbs(crop,alpha=.9),cv2.convertScaleAbs(crop,alpha=1.1)]
            model.train(images,np.zeros(3,dtype=np.int32));model.write(str(target));return {'match':True,'message':'Visage enregistré localement (expérimental)'}
        if not target.exists():return {'match':False,'message':'Enregistre d’abord ton visage'}
        model.read(str(target));_,distance=model.predict(crop);return {'match':bool(distance<65),'distance':float(distance)}
    if action.endswith('voice'):
        from resemblyzer import VoiceEncoder,preprocess_wav
        wave=np.frombuffer(base64.b64decode(d['audio']),dtype='<f4').copy()
        if len(wave)<int(d['rate'])*2 or not np.isfinite(wave).all():raise ValueError('Au moins 2 secondes de voix sont nécessaires')
        if np.sqrt(np.mean(wave**2))<.005:return {'match':False,'message':'Enregistrement trop silencieux'}
        encoder=VoiceEncoder(device='cpu',verbose=False)
        wav=preprocess_wav(wave,source_sr=int(d['rate']))
        if len(wav)<16000:raise ValueError('Pas assez de parole détectée')
        embedding=encoder.embed_utterance(wav);target=folder/'voice.npy'
        if action=='enroll_voice':np.save(target,embedding);return {'match':True,'message':'Voix enregistrée localement (expérimental)'}
        if not target.exists():return {'match':False,'message':'Enregistre d’abord ta voix'}
        ref=np.load(target,allow_pickle=False);score=float(np.dot(ref,embedding)/(np.linalg.norm(ref)*np.linalg.norm(embedding)))
        return {'match':bool(score>.78),'similarity':score}
    raise ValueError('Action inconnue')
if __name__=='__main__':
    try:
        # Some ML dependencies print to stdout; reserve stdout for JSON.
        import contextlib
        with contextlib.redirect_stdout(sys.stderr):result=main(json.load(sys.stdin))
        print(json.dumps(result))
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
