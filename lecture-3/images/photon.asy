import three;
import math;
import graph3;
import contour;
import tube;
import fontsize;
import settings;
outformat="html";

//size(16cm);
//size3(16cm,16cm,16cm);
//defaultrender=render(compression=Zero,merge=true);

currentprojection=orthographic(4,6,3);

currentprojection=perspective(10,-10,3,center=true);
//currentprojection=perspective(15,-8.5,n/2+0.5,center=true);
//light lit=currentlight;

size3(24cm, 24cm, 24cm);
//size3(200,IgnoreAspect);


real cc(real t) {return cos(2pi*t);}
real ss(real t) {return sin(2pi*t);}
real tt(real t) {return t;}
real zero(real t) {return 0;}

path3 p1=graph(tt,ss,zero,0,3,operator ..);
path3 p2=graph(tt,zero,cc,0,3,operator ..);
path3 px=graph(tt, zero, zero, 0, 3, operator --);

draw(p1,linewidth(3)+rgb(0,0,1), Arrow3);
draw(p2,linewidth(3)+rgb(0,1,0), Arrow3);
draw(px,linewidth(3)+gray(0.3), Arrow3(0, 0));


scale(true);

label("$|0\rangle$",(tt(0.75),ss(0.75),0),SW, fontsize(32));
label("$|1\rangle$",(tt(0.5),0, cc(0.5)),SW, fontsize(32));

xaxis3(XZ()*"$x$",Bounds,gray(0.5)+linewidth(1.5),InTicks(Label,2,2));
yaxis3(YZ()*"$y$",Bounds,gray(0.5)+linewidth(1.5),InTicks(beginlabel=false,Label,2,2));
zaxis3(XZ()*"$z$",Bounds,gray(0.5)+linewidth(1.5),InTicks(Label,2,2));

//filldraw(p1^^px);
//import bsp;
//face[] faces;
//p1 = p1--cycle;
//filldraw(faces.push(p1), project(p1), yellow);
//add(faces);