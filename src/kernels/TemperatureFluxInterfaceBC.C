#include "TemperatureFluxInterfaceBC.h"

registerMooseObject("purpleApp", TemperatureFluxInterfaceBC);

InputParameters
TemperatureFluxInterfaceBC::validParams()
{
  InputParameters params = ADNodalBC::validParams();

  // Specify input parameters that we want users to be able to set:
  params.addParam<Real>("interface_conductance", "Interface conductance constant");
  params.addRequiredCoupledVar("sample_temp", "corresponding z-component flux variable");
  params.addRequiredCoupledVar("transducer_temp", "Neighbor temperature variable");
  return params;
}

TemperatureFluxInterfaceBC::TemperatureFluxInterfaceBC(const InputParameters & parameters)
  : ADNodalBC(parameters),
    // store the user-specified parameters from the input file...
	_conductance(getParam<Real>("interface_conductance")),
	_temp_samp(adCoupledValue("sample_temp")),
	_temp_trans(adCoupledValue("transducer_temp"))
	
{
}

ADReal
TemperatureFluxInterfaceBC::computeQpResidual()
{
  // For dirichlet BCS, u=BC at the boundary, so the residual includes _u and the desired BC value:
  ADReal return_val = -_conductance * (_temp_samp[_qp] - _temp_trans[_qp]);
  
  return (_u - return_val);
}