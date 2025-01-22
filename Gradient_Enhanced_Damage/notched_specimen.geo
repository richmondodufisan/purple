// Gmsh project created on Tue Mar 12 02:51:52 2024
SetFactory("OpenCASCADE");
//+
refinement = 5;
//+
Point(1) = {500, 500, 0, refinement};
//+
Point(2) = {-500, 500, 0, refinement};
//+
Point(3) = {-500, -500, 0, refinement};
//+
Point(4) = {500, -500, 0, refinement};
//+
Point(5) = {-400, -400, 0, refinement};
//+
Point(6) = {400, 400, 0, refinement};
//+
Point(7) = {-250, -500, 0, refinement};
//+
Point(8) = {-500, -250, 0, refinement};
//+
Point(9) = {500, 250, 0, refinement};
//+
Point(10) = {250, 500, 0, refinement};
//+
Line(1) = {2, 8};
//+
Line(2) = {2, 10};
//+
Line(3) = {9, 4};
//+
Line(4) = {4, 7};
//+
Circle(5) = {8, 5, 7};
//+
Circle(6) = {10, 6, 9};
//+
Physical Curve("sides", 7) = {1};
//+
Physical Curve("load_surface", 8) = {2};
//+
Physical Curve("fixed_surface", 9) = {4, 3};
//+
Curve Loop(1) = {2, 6, 3, 4, -5, -1};
//+
Plane Surface(1) = {1};
