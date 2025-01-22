// Gmsh project created on Tue Mar 05 16:05:00 2024
SetFactory("OpenCASCADE");
//+
regular=100.0;
//+
refine=15.0;
//+
Point(1) = {-1000, -25, 0, regular};
//+
Point(2) = {-1000, 25, 0, regular};
//+
Point(3) = {1000, 25, 0, regular};
//+
Point(4) = {1000, -25, 0, regular};
//+
Point(5) = {1000, -25, 200, regular};
//+
Point(6) = {1000, 25, 200, regular};
//+
Point(7) = {-1000, -25, 200, regular};
//+
Point(8) = {-1000, 25, 200, regular};
//+
Point(9) = {-10, 25, 0, refine};
//+
Point(10) = {-10, -25, 0, refine};
//+
Point(11) = {10, -25, 0, refine};
//+
Point(12) = {10, 25, 0, refine};
//+
Point(13) = {10, 25, 100, refine};
//+
Point(14) = {10, -25, 100, refine};
//+
Point(15) = {-10, -25, 100, refine};
//+
Point(16) = {-10, 25, 100, refine};
//+
Line(1) = {1, 2};
//+
Line(2) = {1, 7};
//+
Line(3) = {7, 8};
//+
Line(4) = {8, 2};
//+
Line(5) = {1, 10};
//+
Line(6) = {10, 15};
//+
Line(7) = {15, 14};
//+
Line(8) = {14, 11};
//+
Line(9) = {11, 4};
//+
Line(10) = {4, 5};
//+
Line(11) = {5, 7};
//+
Line(12) = {8, 6};
//+
Line(13) = {6, 5};
//+
Line(14) = {3, 4};
//+
Line(15) = {3, 12};
//+
Line(16) = {12, 13};
//+
Line(17) = {13, 16};
//+
Line(18) = {16, 9};
//+
Line(19) = {9, 2};
//+
Line(20) = {10, 9};
//+
Line(21) = {15, 16};
//+
Line(22) = {14, 13};
//+
Line(23) = {11, 12};
//+
Line(24) = {3, 6};
//+
Curve Loop(1) = {5, 6, 7, 8, 9, 10, 11, -2};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {12, -24, 15, 16, 17, 18, 19, -4};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {12, 13, 11, 3};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {10, -13, -24, 14};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {4, -1, 2, 3};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {16, -22, 8, 23};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {17, -21, 7, 22};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {18, -20, 6, 21};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {19, -1, 5, 20};
//+
Plane Surface(9) = {9};
//+
Curve Loop(10) = {9, -14, 15, -23};
//+
Plane Surface(10) = {10};
//+
Surface Loop(1) = {2, 3, 4, 1, 9, 5, 8, 7, 6, 10};
//+
Volume(1) = {1};
//+
Point(17) = {-100, 25, 0, refine};
//+
Point(18) = {-100, -25, 0, refine};
//+
Point(19) = {100, -25, 0, refine};
//+
Point(20) = {100, 25, 0, refine};
//+
Point(21) = {100, 25, 200, refine};
//+
Point(22) = {100, -25, 200, refine};
//+
Point(23) = {-100, -25, 200, refine};
//+
Point(24) = {-100, 25, 200, refine};
//+
Line(25) = {17, 18};
//+
Line(26) = {18, 10};
//+
Line(27) = {17, 9};
//+
Line(28) = {19, 20};
//+
Line(29) = {19, 11};
//+
Line(30) = {20, 12};
//+
Line(31) = {24, 23};
//+
Line(32) = {21, 22};
//+
Line(33) = {23, 22};
//+
Line(34) = {24, 21};
//+
Line(35) = {23, 18};
//+
Line(36) = {24, 17};
//+
Line(37) = {21, 20};
//+
Line(38) = {22, 19};
//+
Curve Loop(11) = {33, 38, 29, -8, -7, -6, -26, -35};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {34, 37, 30, 16, 17, 18, -27, -36};
//+
Plane Surface(12) = {12};
//+
Curve Loop(13) = {35, -25, -36, 31};
//+
Plane Surface(13) = {13};
//+
Curve Loop(14) = {32, 38, 28, -37};
//+
Plane Surface(14) = {14};
//+
Curve Loop(15) = {29, 23, -30, -28};
//+
Plane Surface(15) = {15};
//+
Curve Loop(16) = {26, 20, -27, 25};
//+
Plane Surface(16) = {16};
//+
Curve Loop(17) = {6, 21, 18, -20};
//+
Plane Surface(17) = {17};
//+
Curve Loop(18) = {8, 23, 16, -22};
//+
Plane Surface(18) = {18};
//+
Curve Loop(19) = {7, 22, 17, -21};
//+
Plane Surface(19) = {19};
//+
Curve Loop(20) = {33, -32, -34, 31};
//+
Plane Surface(20) = {20};
//+
Surface Loop(2) = {20, 11, 14, 15, 12, 16, 13, 17, 18, 19};
//+
Volume(2) = {2};
//+
Point(27) = {0, 25, 200, refine};
//+
Point(28) = {0, -25, 200, refine};
//+
Line(41) = {28, 27};
//+
Coherence;
//+
Physical Curve("top-line", 82) = {41};
//+
Physical Curve("bottom-left", 83) = {46};
//+
Physical Curve("bottom-right", 84) = {61};
