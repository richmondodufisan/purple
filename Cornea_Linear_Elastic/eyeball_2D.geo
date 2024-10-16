// Gmsh project created on Wed Oct 16 11:42:37 2024
SetFactory("OpenCASCADE");
//+
Point(1) = {0, 0, 0, 0.00005};
//+
Point(2) = {0.002, 0, 0, 0.00005};
//+
Point(3) = {-0.002, 0, 0, 0.00005};
//+
Point(4) = {0, -0.002, 0, 0.00005};
//+
Point(5) = {0, 0.002, 0, 0.00005};
//+
Circle(1) = {5, 1, 2};
//+
Circle(2) = {2, 1, 4};
//+
Circle(3) = {4, 1, 3};
//+
Circle(4) = {3, 1, 5};
//+
Curve Loop(1) = {4, 1, 2, 3};
//+
Plane Surface(1) = {1};
//+
Physical Point("loading_point", 5) = {5};
