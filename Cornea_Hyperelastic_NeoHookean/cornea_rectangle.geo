// Gmsh project created on Wed Mar 27 12:03:52 2024
SetFactory("OpenCASCADE");
//+
refinement = 0.000025;
//+
Point(1) = {0, 0, 0, refinement};
//+
Point(2) = {0.02, 0, 0, refinement};
//+
Point(3) = {0.02, 0.001, 0, refinement};
//+
Point(4) = {0, 0.001, 0, refinement};
//+
Point(5) = {0.002, 0.001, 0, refinement};
//+
Line(1) = {4, 1};
//+
Line(2) = {1, 2};
//+
Line(3) = {2, 3};
//+
Line(4) = {3, 5};
//+
Line(5) = {5, 4};
//+
Curve Loop(1) = {5, 1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Physical Curve("top", 6) = {4, 5};
//+
Physical Curve("bottom", 7) = {2};
//+
Physical Curve("left", 8) = {1};
//+
Physical Curve("right", 9) = {3};
//+
Physical Point("loading_point", 10) = {4};
//+
Physical Point("data_point", 11) = {5};
