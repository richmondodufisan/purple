
#pragma once

#include "ADTimeDerivative.h"

class DiffusionTemperatureTimeDerivative : public ADTimeDerivative
{
public:
  static InputParameters validParams();

  DiffusionTemperatureTimeDerivative(const InputParameters & parameters);

protected:
  virtual ADReal precomputeQpResidual() override;

  // Specific heat material property
  const ADMaterialProperty<Real> & _rho_c;
};
