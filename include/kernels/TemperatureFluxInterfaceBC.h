#pragma once

#include "ADNodalBC.h"

class TemperatureFluxInterfaceBC : public ADNodalBC
{
public:
  TemperatureFluxInterfaceBC(const InputParameters & parameters);

  static InputParameters validParams();

protected:
  virtual ADReal computeQpResidual() override;

private:
  // Required variables and constants
  Real _conductance;
  const ADVariableValue & _temp_samp;
  const ADVariableValue & _temp_trans;
  
};