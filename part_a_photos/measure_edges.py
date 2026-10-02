#!/usr/bin/env python3
"""PART A EDGE AND ANGLE MEASUREMENT FROM THE CLASS CRYSTAL PHOTOGRAPHS.

picture1.jpg   10 CRYSTALS C1..C10 (picture2.jpg IS THE SAME LAYOUT, RETAKEN)
picture3-5.jpg ONE CRYSTAL PHOTOGRAPHED ALONE IN THREE POSES (VIEWS A, B, C)

METHOD: CROP EACH CRYSTAL AT FULL RESOLUTION, CLAHE CONTRAST, GAUSSIAN BLUR 1.6 px,
OPENCV LINE SEGMENT DETECTOR (LSD), KEEP SEGMENTS OF 28 px OR MORE. THE SEGMENTS THAT
LIE ON CRYSTAL EDGES (NOT SHADOW EDGES OR INTERNAL CRACKS) ARE CHOSEN BY HAND IN SEL
BELOW, AFTER VIEWING THE NUMBERED OVERLAYS WRITTEN TO overlays/. EACH EDGE FAMILY IS A
LENGTH-WEIGHTED CIRCULAR MEAN; A CORNER IS THE ACUTE ANGLE BETWEEN THE PRISM-EDGE
FAMILY AND ONE END FAMILY, SO 90 MEANS A RIGHT ANGLE.
"""
import cv2, numpy as np, json, os
HERE=os.path.dirname(os.path.abspath(__file__))
S=3072/900          # CENTRES BELOW ARE GIVEN ON A 900 x 1200 PREVIEW
P1=[(115,105),(760,155),(190,410),(665,415),(230,688),(600,700),(318,925),(518,942),(335,1112),(458,1125)]
ISO={3:(445,600),4:(463,662),5:(430,715)}
SEL={ # PRISM-EDGE SEGMENT IDS ; END GROUPS ; READING
 'C1':([0,10],{'TOP':[5,9],'BOT':[3,7]},'CLEAN'),
 'C2':([11,3],{'END':[0,5]},'CLEAN, NEAR-EQUANT'),
 'C3':([0,3,4,10],{'END':[6,5,7,14,19]},'CLEAN, TOP + SIDE FACE'),
 'C4':([1,8,0,3],{'RIGHT':[2,5],'LEFT':[10]},'RIGHT CLEAN, LEFT ROUNDED'),
 'C6':([1,8,6],{'LEFT':[0],'RIGHT':[3,4]},'CLEAN'),
 'C7':([1,13,5,6],{'END':[0,10,17]},'CLEAN'),
 'C8':([9,11,3,6],{'TOP':[0],'BOT':[1]},'TOP CLEAN, BOTTOM ROUNDED'),
 'C9':([16,6,4,1],{'LEFT':[5,7,8],'RIGHT':[3,0]},'RIGHT CLEAN, LEFT CHIPPED'),
 'C10':([10,14,2,5,3],{'UR':[8],'LL':[6]},'BOTH ENDS CHIPPED'),
 'PIC4':([2,0,1,7],{'TOP':[4],'BOT':[6,11]},'BOTTOM CLEAN, TOP ROUGH'),
}
CLEAN={'C1':['TOP','BOT'],'C2':['END'],'C3':['END'],'C4':['RIGHT'],'C6':['LEFT','RIGHT'],
       'C7':['END'],'C8':['TOP'],'C9':['RIGHT'],'PIC4':['BOT']}
def lsd(img,cx,cy,r,minlen):
    X,Y=int(cx*S),int(cy*S); crop=img[Y-r:Y+r,X-r:X+r]
    g=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
    cl=cv2.createCLAHE(clipLimit=3.0,tileGridSize=(4,4)).apply(g)
    L=cv2.createLineSegmentDetector(cv2.LSD_REFINE_STD).detect(cv2.GaussianBlur(cl,(0,0),1.6))[0]
    segs=[[float(v) for v in s] for s in L.reshape(-1,4) if np.hypot(s[2]-s[0],s[3]-s[1])>=minlen]
    return segs,(X-r,Y-r),cl
def info(s):
    x1,y1,x2,y2=s
    return np.degrees(np.arctan2(y2-y1,x2-x1))%180, np.hypot(x2-x1,y2-y1)
def fam(ids,segs):
    A=[info(segs[i]) for i in ids]
    m=(np.degrees(np.angle(sum(L*np.exp(2j*np.radians(a)) for a,L in A)))/2)%180
    dev=[((a-m+90)%180)-90 for a,_ in A]
    return m,max(dev)-min(dev)
if __name__=='__main__':
    os.makedirs(HERE+'/overlays',exist_ok=True)
    out={}
    im1=cv2.imread(HERE+'/picture1.jpg')
    jobs=[(f'C{k+1}',im1,x,y,190,28) for k,(x,y) in enumerate(P1)]
    jobs+=[(f'PIC{i}',cv2.imread(HERE+f'/picture{i}.jpg'),x,y,250,34) for i,(x,y) in ISO.items()]
    for name,img,x,y,r,ml in jobs:
        segs,org,cl=lsd(img,x,y,r,ml)
        up=cv2.resize(cv2.cvtColor(cl,cv2.COLOR_GRAY2BGR),None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
        for k,(x1,y1,x2,y2) in enumerate(segs):
            cv2.line(up,(int(2*x1),int(2*y1)),(int(2*x2),int(2*y2)),(0,0,255),2)
            cv2.putText(up,str(k),(int(x1+x2)+3,int(y1+y2)-3),cv2.FONT_HERSHEY_SIMPLEX,0.55,(0,0,255),2)
        cv2.imwrite(f'{HERE}/overlays/{name}.jpg',up,[cv2.IMWRITE_JPEG_QUALITY,85])
        rec={'origin':org,'r':r,'segs':segs}
        if name in SEL:
            lids,ends,read=SEL[name]; m,spread=fam(lids,segs)
            u=np.array([np.cos(np.radians(m)),np.sin(np.radians(m))]); n=np.array([-u[1],u[0]])
            ids=lids+[i for v in ends.values() for i in v]
            P=np.array([p for i in ids for p in (segs[i][:2],segs[i][2:])])
            Lx,Wx=np.ptp(P@u),np.ptp(P@n)
            rec.update(prism=lids,prism_dir=round(m,2),parallel_spread=round(spread,1),
                       aspect=round(max(Lx,Wx)/min(Lx,Wx),2),reading=read,ends={})
            for nm,e_ids in ends.items():
                e,_=fam(e_ids,segs); rec['ends'][nm]={'ids':e_ids,'dir':round(e,2),
                    'corner':round(abs(((e-m+90)%180)-90),1),'clean':nm in CLEAN.get(name,[])}
        out[name]=rec
    cl=[e['corner'] for v in out.values() for e in v.get('ends',{}).values() if e['clean']]
    ob=[e['corner'] for v in out.values() for e in v.get('ends',{}).values() if not e['clean']]
    out['_summary']={'clean_n':len(cl),'clean_mean':round(float(np.mean(cl)),2),'clean_sd':round(float(np.std(cl,ddof=1)),2),
                     'clean_min':min(cl),'clean_max':max(cl),'oblique':sorted(ob),
                     'aspect':sorted(v['aspect'] for k,v in out.items() if 'aspect' in v)}
    json.dump(out,open(HERE+'/measure.json','w'),indent=1)
    print(json.dumps(out['_summary']))
    for k,v in out.items():
        if 'ends' in v: print(k,v['aspect'],v['parallel_spread'],{n:(e['corner'],e['clean']) for n,e in v['ends'].items()},v['reading'])
