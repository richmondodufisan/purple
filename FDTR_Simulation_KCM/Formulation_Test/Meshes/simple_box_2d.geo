// Gmsh project created on Fri Dec 01 19:50:52 2023
SetFactory("OpenCASCADE");
//+
Point(1) = {0, 0, 0, 0.3};
//+
Point(2) = {0, 20, 0, 0.3};
//+
Point(3) = {20, 20, 0, 0.3};
//+
Point(4) = {20, 0, 0, 0.3};
//+
Line(1) = {2, 3};
//+
Line(2) = {3, 4};
//+
Line(3) = {4, 1};
//+
Line(4) = {1, 2};
//+
Physical Curve("left", 5) = {4};
//+
Physical Curve("right", 6) = {2};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
