#include "TotalLagrangianStressDivergenceIncompressibleHyperelasticity.h"

registerMooseObject("purpleApp", TotalLagrangianStressDivergenceIncompressibleHyperelasticity);



template <class G>
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase(
    const InputParameters & parameters)
  : LagrangianStressDivergenceBase(parameters),
    _pk1(getMaterialPropertyByName<RankTwoTensor>(_base_name + "pk1_stress")),
    _dpk1(getMaterialPropertyByName<RankFourTensor>(_base_name + "pk1_jacobian")),
	
	
	
	
	
	
	////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
	_mu(getParam<Real>("mu")),    
    _p_var(coupled("pressure")),           
    _p(coupledValue("pressure"))    
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	
	
	
	
	
	
	
{
}

template <class G>
RankTwoTensor
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::gradTest(unsigned int component)
{
  // F-bar doesn't modify the test function
  return G::gradOp(component, _grad_test[_i][_qp], _test[_i][_qp], _q_point[_qp]);
}

template <class G>
RankTwoTensor
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::gradTrial(unsigned int component)
{
  return _stabilize_strain ? gradTrialStabilized(component) : gradTrialUnstabilized(component);
}

template <class G>
RankTwoTensor
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::gradTrialUnstabilized(unsigned int component)
{
  // Without F-bar stabilization, simply return the gradient of the trial functions
  return G::gradOp(component, _grad_phi[_j][_qp], _phi[_j][_qp], _q_point[_qp]);
}

template <class G>
RankTwoTensor
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::gradTrialStabilized(unsigned int component)
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










////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////IRRELEVANT, ignore //////////////////////////////////////////////////////////////////////

template <class G>
void
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::precalculateJacobianDisplacement(unsigned int component)
{
  // For total Lagrangian, the averaging is taken on the reference frame regardless of geometric
  // nonlinearity. Convenient!
  for (auto j : make_range(_phi.size()))
    _avg_grad_trial[component][j] = StabilizationUtils::elementAverage(
        [this, component, j](unsigned int qp)
        { return G::gradOp(component, _grad_phi[j][qp], _phi[j][qp], _q_point[qp]); },
        _JxW,
        _coord);
}

template <class G>
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpResidual()
{
  return gradTest(_alpha).doubleContraction(_pk1[_qp]);
}

template <class G>
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpJacobianDisplacement(unsigned int alpha,
                                                                      unsigned int beta)
{
  // J_{alpha beta} = phi^alpha_{i, J} T_{iJkL} G^beta_{kL}
  return gradTest(alpha).doubleContraction(_dpk1[_qp] * gradTrial(beta));
}

template <class G>
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpJacobianTemperature(unsigned int cvar)
{
  usingTensorIndices(i_, j_, k_, l_);
  // Multiple eigenstrains may depend on the same coupled var
  RankTwoTensor total_deigen;
  for (const auto deigen_darg : _deigenstrain_dargs[cvar])
    total_deigen += (*deigen_darg)[_qp];

  const auto A = _f_inv[_qp].inverse();
  const auto B = _F_inv[_qp].inverse();
  const auto U = 0.5 * (A.template times<i_, k_, l_, j_>(B) + A.template times<i_, l_, k_, j_>(B));

  return -(_dpk1[_qp] * U * total_deigen).doubleContraction(gradTest(_alpha)) *
         _temperature->phi()[_j][_qp];
}

template <class G>
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpJacobianOutOfPlaneStrain()
{
  return _dpk1[_qp].contractionKl(2, 2, gradTest(_alpha)) * _out_of_plane_strain->phi()[_j][_qp];
}



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

























////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
/// **Residual computation**
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpResidual()
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
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpJacobian()
{
  return gradTest(_alpha).doubleContraction(_dpk1[_qp] * gradTrial(_alpha));
}

/// **Off-diagonal Jacobian computation**
Real
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<G>::computeQpOffDiagJacobian(unsigned int jvar)
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



























template class TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<GradientOperatorCartesian>;
