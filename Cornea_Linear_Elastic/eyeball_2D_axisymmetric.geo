// Gmsh project created on Wed Oct 16 21:57:06 2024
SetFactory("OpenCASCADE");
refinement = 0.0002;
//+
Point(1) = {0, 0, 0, refinement};
//+
Point(2) = {0, 0, 0.002, refinement};
//+
Point(3) = {0, 0, -0.002, refinement};
//+
Point(4) = {0.002, 0, 0, refinement};
//+
Circle(1) = {2, 1, 4};
//+
Circle(2) = {3, 1, 4};
//+
Line(3) = {2, 1};
//+
Line(4) = {1, 3};
//+
Curve Loop(1) = {3, 4, 2, -1};
//+
Plane Surface(1) = {1};
//+
Physical Point("loading_point", 5) = {2};
//+
Physical Curve("sample_location", 6) = {1};
