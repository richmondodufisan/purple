#include "ComputeStressNeoHookean.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStressNeoHookean);

InputParameters
ComputeStressNeoHookean::validParams()
{
  InputParameters params = ComputeLagrangianStressPK1::validParams();
  params.addClassDescription("Calculate PK1 Stress for Neo Hookean Model");

  return params;
}

ComputeStressNeoHookean::ComputeStressNeoHookean(const InputParameters & parameters)
  : ComputeLagrangianStressPK1(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),
	
	_dWdF_in(getMaterialPropertyByName<RankTwoTensor>(_base_name + "dWdF")),	// this is the stress
	_d2WdF2_in(getMaterialPropertyByName<RankFourTensor>(_base_name + "d2WdF2")) //this is the tangent operator


{
}


void
ComputeStressNeoHookean::computeQpPK1Stress()
{
	_pk1_stress[_qp] = _dWdF_in[_qp];
	
	_pk1_jacobian[_qp] = _d2WdF2_in[_qp];
	
}


