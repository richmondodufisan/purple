#pragma once

#include "ADNodalBC.h"

class MatchedValueNegativeBC : public ADNodalBC
{
public:
  MatchedValueNegativeBC(const InputParameters & parameters);

  static InputParameters validParams();

protected:
  virtual ADReal computeQpResidual() override;

private:
  // Required variables and constants
  const ADVariableValue & _coupled_var;
};
