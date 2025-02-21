#include "TotalLagrangianStressDivergenceIncompressibleHyperelasticity.h"

registerMooseObject("purpleApp", TotalLagrangianStressDivergenceIncompressibleHyperelasticity);

/// **ValidParams specialization for Cartesian coordinates**
template <>
InputParameters
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<GradientOperatorCartesian>::validParams()
{
  InputParameters params = TotalLagrangianStressDivergenceBase<GradientOperatorCartesian>::validParams();
  params.addClassDescription("Enforce equilibrium with a total Lagrangian formulation in Cartesian coordinates.");
  params.addRequiredParam<Real>("mu", "Shear modulus");
  params.addRequiredCoupledVar("pressure", "Pressure variable (coupled)");
  return params;
}

/// **initialSetup() specialization for Cartesian coordinates**
template <>
void
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<GradientOperatorCartesian>::initialSetup()
{
  if (this->getBlockCoordSystem() != Moose::COORD_XYZ)
    mooseError("This kernel should only act in Cartesian coordinates.");
}

/// **Constructor**
template <class G>
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase(
    const InputParameters & parameters)
  : TotalLagrangianStressDivergenceBase<G>(parameters),
    _mu(this->template getParam<Real>("mu")),    
    _p_var(this->coupled("pressure")),          
    _p(this->coupledValue("pressure"))          
{
}

/// **Residual computation**
template <class G>
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpResidual()
{
  RankTwoTensor F_inv_T = this->_F_inv[this->_qp].transpose();
  Real J = this->_F[this->_qp].det();
  Real p_val = this->_p[this->_qp];

  // Compute modified PK1 stress
  RankTwoTensor P_custom = this->_mu * (this->_F[this->_qp] - F_inv_T) - p_val * J * F_inv_T;

  // Compute residual using MOOSE’s gradTest
  return this->gradTest(this->_alpha).doubleContraction(P_custom);
}

/// **Jacobian computation**
template <class G>
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpJacobian()
{
  return this->gradTest(this->_alpha).doubleContraction(this->_dpk1[this->_qp] * this->gradTrial(this->_alpha));
}

/// **Off-diagonal Jacobian computation**
template <class G>
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpOffDiagJacobian(unsigned int jvar)
{
  // If jvar corresponds to pressure, compute the off-diagonal Jacobian
  if (jvar == this->_p_var)
  {
    RankTwoTensor dP_dp = -this->_F[this->_qp].det() * this->_F_inv[this->_qp].transpose();
    return this->gradTest(this->_alpha).doubleContraction(dP_dp);
  }

  // If jvar corresponds to displacement, use MOOSE's structure for displacement coupling
  for (unsigned int beta = 0; beta < this->_ndisp; beta++)
    if (jvar == this->_disp_nums[beta])
      return this->gradTest(this->_alpha).doubleContraction(this->_dpk1[this->_qp] * this->gradTrial(beta));

  return 0;
}

/// **Explicit template instantiation**
template class TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<GradientOperatorCartesian>;
