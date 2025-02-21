#include "TotalLagrangianStressDivergenceIncompressibleHyperelasticity.h"

registerMooseObject("purpleApp", TotalLagrangianStressDivergenceIncompressibleHyperelasticity);


InputParameters
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::validParams()
{
  InputParameters params = TotalLagrangianStressDivergenceIncompressibleHyperelasticity::validParams();
  params.addClassDescription("Enforce equilibrium with a total Lagrangian formulation in Cartesian coordinates.");
  params.addRequiredParam<Real>("mu", "Shear modulus");
  params.addRequiredCoupledVar("pressure", "Pressure variable (coupled)");
  return params;
}


/// **Constructor**
template <class G>
TotalLagrangianStressDivergenceIncompressibleHyperelasticity::TotalLagrangianStressDivergenceIncompressibleHyperelasticity(
    const InputParameters & parameters)
  : TotalLagrangianStressDivergenceBase<G>(parameters),
    _mu(getParam<Real>("mu")),    
    _p_var(coupled("pressure")),          
    _p(coupledValue("pressure"))          
{
}

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
