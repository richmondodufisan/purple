//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html

#include "TotalLagrangianStressDivergenceIncompressibleHyperelasticity.h"

InputParameters
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::validParams()
{
  InputParameters params = Kernel::validParams();

  params.addRequiredParam<unsigned int>("component", "Which direction this kernel acts in");
  params.addRequiredCoupledVar("displacements", "The displacement components");

  params.addParam<bool>("large_kinematics", false, "Use large displacement kinematics");
  params.addParam<bool>("stabilize_strain", false, "Average the volumetric strains");
  
  // This kernel requires use_displaced_mesh to be off
  params.suppressParameter<bool>("use_displaced_mesh");

  params.addParam<std::string>("base_name", "Material property base name");
  
  
  
  
  
  ////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
  params.addClassDescription("Enforce equilibrium with a total Lagrangian formulation in Cartesian coordinates.");
  params.addRequiredParam<Real>("mu", "Shear modulus");
  params.addRequiredCoupledVar("pressure", "Pressure variable (coupled)");
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





  return params;
}

TotalLagrangianStressDivergenceIncompressibleHyperelasticity::TotalLagrangianStressDivergenceIncompressibleHyperelasticity(const InputParameters & parameters)
  : JvarMapKernelInterface<DerivativeMaterialInterface<Kernel>>(parameters),
    _large_kinematics(getParam<bool>("large_kinematics")),
    _stabilize_strain(getParam<bool>("stabilize_strain")),
    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),
    _alpha(getParam<unsigned int>("component")),
    _ndisp(coupledComponents("displacements")),
    _disp_nums(_ndisp),
    _avg_grad_trial(_ndisp),
    _F_ust(
        getMaterialPropertyByName<RankTwoTensor>(_base_name + "unstabilized_deformation_gradient")),
    _F_avg(getMaterialPropertyByName<RankTwoTensor>(_base_name + "average_deformation_gradient")),
    _f_inv(getMaterialPropertyByName<RankTwoTensor>(_base_name +
                                                    "inverse_incremental_deformation_gradient")),
    _F_inv(getMaterialPropertyByName<RankTwoTensor>(_base_name + "inverse_deformation_gradient")),
    _F(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),
	
	
	_pk1(getMaterialPropertyByName<RankTwoTensor>(_base_name + "pk1_stress")),
    _dpk1(getMaterialPropertyByName<RankFourTensor>(_base_name + "pk1_jacobian")),
	
	
	
	
	
	
	////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
	_mu(getParam<Real>("mu")),    
    _p_var(coupled("pressure")),           
    _p(coupledValue("pressure"))    
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	
	


{
  // Do the vector coupling of the displacements
  for (unsigned int i = 0; i < _ndisp; i++)
    _disp_nums[i] = coupled("displacements", i);

  // We need to use identical discretizations for all displacement components
  auto order_x = getVar("displacements", 0)->order();
  for (unsigned int i = 1; i < _ndisp; i++)
  {
    if (getVar("displacements", i)->order() != order_x)
      mooseError("The Lagrangian StressDivergence kernels require equal "
                 "order interpolation for all displacements.");
  }


}




void
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::initialSetup()
{
  if (getBlockCoordSystem() != Moose::COORD_XYZ)
    mooseError("This kernel should only act in Cartesian coordinates.");
}





RankTwoTensor
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::gradTest(unsigned int component)
{
  // F-bar doesn't modify the test function
  return G::gradOp(component, _grad_test[_i][_qp], _test[_i][_qp], _q_point[_qp]);
}

RankTwoTensor
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::gradTrial(unsigned int component)
{
  return _stabilize_strain ? gradTrialStabilized(component) : gradTrialUnstabilized(component);
}

RankTwoTensor
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::gradTrialUnstabilized(unsigned int component)
{
  // Without F-bar stabilization, simply return the gradient of the trial functions
  return G::gradOp(component, _grad_phi[_j][_qp], _phi[_j][_qp], _q_point[_qp]);
}

RankTwoTensor
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::gradTrialStabilized(unsigned int component)
{
  // The base unstabilized trial function gradient
  const auto Gb = G::gradOp(component, _grad_phi[_j][_qp], _phi[_j][_qp], _q_point[_qp]);
  // The average trial function gradient
  const auto Ga = _avg_grad_trial[component][_j];

  // The F-bar stabilization depends on kinematics
  if (_large_kinematics)
  {
    // Horrible thing, see the documentation for how we get here
    const Real dratio = std::pow(_F_avg[_qp].det() / _F_ust[_qp].det(), 1.0 / 3.0);
    const Real fact = (_F_avg[_qp].inverse().transpose().doubleContraction(Ga) -
                       _F_ust[_qp].inverse().transpose().doubleContraction(Gb)) /
                      3.0;
    return dratio * (Gb + fact * _F_ust[_qp]);
  }

  // The small kinematics modification is linear
  return Gb + (Ga.trace() - Gb.trace()) / 3.0 * RankTwoTensor::Identity();
}













////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
/// **Residual computation**
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::computeQpResidual()
{
  RankTwoTensor F_inv_T = _F_inv[_qp].transpose();
  Real J = _F[_qp].det();
  Real p_val = _p[_qp];

  // Compute modified PK1 stress
  RankTwoTensor P_custom = _mu * (_F[_qp] - F_inv_T) - p_val * J * F_inv_T;

  // Compute residual using MOOSE’s gradTest
  return gradTest(_alpha).doubleContraction(P_custom);
}

/// **Jacobian computation**
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::computeQpJacobian()
{
  return gradTest(_alpha).doubleContraction(_dpk1[_qp] * gradTrial(_alpha));
}

/// **Off-diagonal Jacobian computation**
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::computeQpOffDiagJacobian(unsigned int jvar)
{
  // If jvar corresponds to pressure, compute the off-diagonal Jacobian
  if (jvar == _p_var)
  {
    RankTwoTensor dP_dp = -_F[_qp].det() * _F_inv[_qp].transpose();
    return gradTest(_alpha).doubleContraction(dP_dp);
  }

  // If jvar corresponds to displacement, use MOOSE's structure for displacement coupling
  for (unsigned int beta = 0; beta < _ndisp; beta++)
    if (jvar == _disp_nums[beta])
      return gradTest(_alpha).doubleContraction(_dpk1[_qp] * gradTrial(beta));

  return 0;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////






