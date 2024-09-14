#include "ComputeStressIncompressible.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStressIncompressible);

InputParameters
ComputeStressIncompressible::validParams()
{
  InputParameters params = ComputeLagrangianStressPK1::validParams();
  params.addClassDescription("Calculate PK1 Stress for an incompressible material based on its strain energy");

  return params;
}

ComputeStressIncompressible::ComputeStressIncompressible(const InputParameters & parameters)
  : ComputeLagrangianStressPK1(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),
	
	_dWdF_pF_in(getMaterialPropertyByName<RankTwoTensor>(_base_name + "dWdF_pF")),	
	_dPK1_dW_in(getMaterialPropertyByName<RankFourTensor>(_base_name + "dPK1_dW")) 


{
}


void
ComputeStressIncompressible::computeQpPK1Stress()
{
	_pk1_stress[_qp] = _dWdF_pF_in[_qp];
	
	_pk1_jacobian[_qp] = _dPK1_dW_in[_qp];
	
}


