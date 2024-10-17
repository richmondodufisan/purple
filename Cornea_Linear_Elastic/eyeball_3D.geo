// Gmsh project created on Wed Oct 16 19:47:43 2024
SetFactory("OpenCASCADE");
refinement = 0.00005;
//+
Point(1) = {0, 0, 0, refinement};
//+
Point(2) = {0, 0.002, 0, refinement};
//+
Point(3) = {0, -0.002, 0, refinement};
//+
Point(4) = {0, 0, 0.002, refinement};
//+
Point(5) = {0, 0, -0.002, refinement};
//+
Point(6) = {0.002, 0, 0, refinement};
//+
Point(7) = {-0.002, 0, 0, refinement};
//+
Circle(1) = {4, 1, 2};
//+
Circle(2) = {2, 1, 5};
//+
Circle(3) = {6, 1, 2};
//+
Circle(4) = {2, 1, 7};
//+
Circle(5) = {4, 1, 3};
//+
Circle(6) = {5, 1, 3};
//+
Circle(7) = {6, 1, 3};
//+
Circle(8) = {7, 1, 3};
//+
Circle(9) = {4, 1, 7};
//+
Circle(10) = {4, 1, 6};
//+
Circle(11) = {6, 1, 5};
//+
Circle(12) = {5, 1, 7};
//+
Curve Loop(2) = {1, -3, -10};
//+
Surface(1) = {2};
//+
Curve Loop(4) = {9, -4, -1};
//+
Surface(2) = {4};
//+
Curve Loop(6) = {2, -11, 3};
//+
Surface(3) = {6};
//+
Curve Loop(8) = {2, 12, -4};
//+
Surface(4) = {8};
//+
Curve Loop(10) = {5, -7, -10};
//+
Surface(5) = {10};
//+
Curve Loop(12) = {7, -6, -11};
//+
Surface(6) = {12};
//+
Curve Loop(14) = {6, -8, -12};
//+
Surface(7) = {14};
//+
Curve Loop(16) = {5, -8, -9};
//+
Surface(8) = {16};
//+
Surface Loop(1) = {7, 6, 5, 1, 2, 4, 3, 8};
//+
Volume(1) = {1};
//+
Surface Loop(2) = {5, 1, 2, 4, 3, 6, 7, 8};
//+
Physical Point("loading_point", 18) = {4};
//+
Physical Curve("sample_location", 19) = {10};
