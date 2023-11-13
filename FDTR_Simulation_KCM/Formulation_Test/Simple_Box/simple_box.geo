//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0, 10, 0, 1.0};
//+
Point(3) = {10, 10, 0, 1.0};
//+
Point(4) = {10, 0, 0, 1.0};
//+
Point(5) = {0, 10, 5, 1.0};
//+
Point(6) = {10, 10, 5, 1.0};
//+
Point(7) = {10, 0, 5, 1.0};
//+
Point(8) = {0, 10, 2.5, 1.0};
//+
Point(9) = {0, 10, 5, 1.0};
//+
Point(10) = {0, 0, 5, 1.0};
//+
Line(1) = {10, 7};
//+
Line(2) = {1, 4};
//+
Line(3) = {4, 7};
//+
Line(4) = {10, 1};
//+
Line(5) = {5, 2};
//+
Line(6) = {2, 1};
//+
Line(7) = {10, 5};
//+
Line(8) = {5, 6};
//+
Line(9) = {6, 7};
//+
Line(10) = {6, 3};
//+
Line(11) = {4, 3};
//+
Line(12) = {3, 2};
//+
Curve Loop(1) = {1, -3, -2, -4};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {3, -9, 10, -11};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {8, 9, -1, 7};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {4, -6, -5, -7};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {12, -5, 8, 10};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {2, 11, 12, 6};
//+
Plane Surface(6) = {6};
//+
Surface Loop(1) = {3, 5, 6, 1, 2, 4};
//+
Volume(1) = {1};
//+
Recursive Delete {
  Point{8}; 
}
//+
Physical Surface("left", 13) = {4};
//+
Physical Surface("right", 14) = {2};
//+
Physical Surface("sides", 15) = {1, 6, 5, 3};
