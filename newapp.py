import streamlit as st
import numpy as np
import pandas as pd
import cv2 as cv
import math
import random

color=[[34,35,227],[0,229,244],[178,113,38],[91,142,0],[1,145,241],[137,56,109],
       [11,198,253],[31,98,234],[125,3,196],[153,78,68],[187,150,6],[38,187,140],
       [2,2,2],[250,250,250],[42,42,191],[255,144,30],[205,0,0],[237,149,100],[225,228,255],
       [240,255,240],[220,220,220],[96,164,244],[193,182,255],[0,235,255],[47,255,173],
       [26,20,21],[69,61,168],[95,85,81],[45,40,37],[66,55,81],[209,109,44],[148,146,146],
       [105,157,207],[165,180,229],[150,158,198],[139,120,127],[149,146,155]]
df=pd.DataFrame({
    'num':[10,5,2]
    })
def findcolor(l):
    for i in range(0,len(color)):
        a=(l[0]-color[i][0])**2
        b=(l[1]-color[i][1])**2
        c=(l[2]-color[i][2])**2
        dev=0.19*a+0.28+b+0.53*c
        if i==0:
            dif=dev
            L=color[i]
        else:
            if dif>dev:
              dif=dev
              L=color[i]
    return L


st.title('图片色块加工')
st.markdown('建议图片尺寸在100-400之间')
upload_file = st.file_uploader(
    label='上传图片'
    )
if upload_file is not None:
    image0 = np.array(bytearray(upload_file.read()),dtype='uint8')
    image0 = cv.imdecode(image0,cv.IMREAD_COLOR)
    st.success("上传成功!")
    h=round(image0.shape[0]/10)*10   #不超过300
    w=round(image0.shape[1]/10)*10   #不超过300
    image0=cv.resize(image0, (w,h)) 
    st.image(image0,channels="BGR")
    frequency=st.selectbox('选择取样频率（仅对像素大于100有效）', df['num'])
    nexT=st.button("像素块化")
    if nexT:
        if 0<h<100:
            m=10
            M=int(h/10)
        else:
            m=math.ceil(h/frequency)
            M=frequency
        if 0<w<100:
            n=10
            N=int(w/10)
        else:
            n=math.ceil(w/frequency)
            N=frequency
        # print(m,n,M,N)  #小写为切块数目，大写为切块尺寸

        drawplace=pd.DataFrame(index=range(m),columns=range(n))  #储存切块位置信息
        drawcolor=pd.DataFrame(index=range(m),columns=range(n))  #储存切块颜色信息
        newimage1=np.zeros([h,w,3],dtype=np.uint8)  #新建画布
        # newimage2=np.zeros([h,w,3],dtype=np.uint8)
        ##信息重组（颜色算法需优化，且有待后续完善与已有颜色的适配）
        for i in range(0,m):
            for j in range(0,n):
                crop=image0[i*M:(i+1)*M,j*N:(j+1)*N]
                drawplace.loc[i,j]=[i*M,(i+1)*M,j*N,(j+1)*N]
                B=np.average(crop[:,:,0])
                G=np.average(crop[:,:,1])
                R=np.average(crop[:,:,2])
                [B,G,R]=findcolor([B,G,R])
                drawcolor.loc[i,j]=[B,G,R]
                tool=random.randint(1,100)
                # print(tool)
                if tool<93:
                    cv.rectangle(newimage1, (j*N,i*M), ((j+1)*N,(i+1)*M),(B,G,R), -1) #画形中先横后纵
                elif tool<98:
                    cv.circle(newimage1 ,(int(j+0.5)*N,int(i+0.5)*M), int(1.3*min(M,N)),(B,G,R),-1)
                else:    
                    cv.line(newimage1,(j*N,i*M),((j+1)*N,(i+1)*M),(B,G,R),int(1*max(M,N)))
        st.image(newimage1,channels="BGR")
        st.header('色块位置(x1,x2,y1,y2)')
        st.write(drawplace)
        st.header('色块BGR')
        st.write(drawcolor)
          
else:
    st.stop()
