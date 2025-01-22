
#pragma once

#include "ADTimeDerivative.h"

class KCMHeatEquationTimeDerivative : public ADTimeDerivative
{
public:
  static InputParameters validParams();

  KCMHeatEquationTimeDerivative(const InputParameters & parameters);

protected:
  virtual ADReal precomputeQpResidual() override;

  // Specific heat material property
  const ADMaterialProperty<Real> & _tau;
};
