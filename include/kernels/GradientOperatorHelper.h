#pragma once

#include "GradientOperator.h"

/// A helper class to access protected methods of GradientOperator
class GradientOperatorHelper : public GradientOperator<GradientOperatorCartesian>
{
public:
  /// Exposes the protected gradOp function to be used in other classes
  using GradientOperator<GradientOperatorCartesian>::gradOp;
};
