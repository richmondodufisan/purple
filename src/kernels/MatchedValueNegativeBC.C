#include "MatchedValueNegativeBC.h"

registerMooseObject("purpleApp", MatchedValueNegativeBC);

InputParameters
MatchedValueNegativeBC::validParams()
{
  InputParameters params = ADNodalBC::validParams();

  // Specify input parameters that we want users to be able to set:
  params.addRequiredCoupledVar("coupled_var", "coupled variable");
  return params;
}

MatchedValueNegativeBC::MatchedValueNegativeBC(const InputParameters & parameters)
  : ADNodalBC(parameters),
    // store the user-specified parameters from the input file...
	_coupled_var(adCoupledValue("coupled_var"))
	
{
}

ADReal
MatchedValueNegativeBC::computeQpResidual()
{
  // For dirichlet BCS, u=BC at the boundary, so the residual includes _u and the desired BC value:
  ADReal return_val = -_coupled_var[_qp];
  
  return (_u - return_val);
}
