#include "TotalLagrangianStressDivergenceOriginal.h"

InputParameters
TotalLagrangianStressDivergenceOriginal::validParams()
{
  InputParameters params = Kernel::validParams();

  params.addRequiredParam<unsigned int>("component", "Which direction this kernel acts in");
  params.addRequiredCoupledVar("displacements", "The displacement components");

  params.addParam<bool>("large_kinematics", false, "Use large displacement kinematics");
  
  // This kernel requires use_displaced_mesh to be off
  params.suppressParameter<bool>("use_displaced_mesh");

  params.addParam<std::string>("base_name", "Material property base name");
  
  
  
  
  
  ////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
  // params.addClassDescription("Enforce equilibrium with a total Lagrangian formulation in Cartesian coordinates.");
  // params.addRequiredParam<Real>("mu", "Shear modulus");
  // params.addRequiredCoupledVar("pressure", "Pressure variable (coupled)");
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





  return params;
}

TotalLagrangianStressDivergenceOriginal::TotalLagrangianStressDivergenceOriginal(const InputParameters & parameters)
  : JvarMapKernelInterface<DerivativeMaterialInterface<Kernel>>(parameters),
    _large_kinematics(getParam<bool>("large_kinematics")),
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
    _dpk1(getMaterialPropertyByName<RankFourTensor>(_base_name + "pk1_jacobian"))
	
	
	
	
	
	
	////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
	// _mu(getParam<Real>("mu")),    
    // _p_var(coupled("pressure")),           
    // _p(coupledValue("pressure"))    
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
TotalLagrangianStressDivergenceOriginal::initialSetup()
{
  if (getBlockCoordSystem() != Moose::COORD_XYZ)
    mooseError("This kernel should only act in Cartesian coordinates.");
}





////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
/// **Residual computation**
Real
TotalLagrangianStressDivergenceOriginal::computeQpResidual()
{
  auto grad_NA = _grad_test[_alpha][_qp];
  auto NA = _test[_alpha][_qp];
  
  
  RankTwoTensor P = _pk1[_qp];
  int i = _alpha;
  
  
  
  Real residual_i = 0.0;
  
  for (int J = 0;  J < _ndisp; ++J)
  {
    residual_i += P(i, J) * grad_NA(J);
  }
  
  
  
  return residual_i;
}

/// **Jacobian computation**
Real
TotalLagrangianStressDivergenceOriginal::computeQpJacobian()
{ 
  // Diagonal Terms of the displacement calculation, i.e A = B -> _alpha = _beta
  auto grad_NA = _grad_test[_alpha][_qp];
  auto NA = _test[_alpha][_qp];
  auto grad_NB = _grad_phi[_alpha][_qp]; // A = B -> _alpha = _beta
  auto NB = _phi[_alpha][_qp];	//A = B -> _alpha = _beta
  
  RankTwoTensor P = _pk1[_qp];
  RankFourTensor dP_dF = _dpk1[_qp];
  int i = _alpha;
  int k = _alpha;	// A = B -> _alpha = _beta
  
  
  Real jacobian_ik = 0.0;

  for (unsigned int J = 0; J < _ndisp; ++J)
  {
      for (unsigned int L = 0; L < _ndisp; ++L) 
      {
        jacobian_ik += grad_NA(J) * dP_dF(i, J, k, L) * grad_NB(L);
      }
  }
  
  return jacobian_ik;
}

/// **Off-diagonal Jacobian computation**
Real
TotalLagrangianStressDivergenceOriginal::computeQpOffDiagJacobian(unsigned int jvar)
{

	
	
  // If jvar corresponds to pressure, compute the off-diagonal Jacobian
  // jvar here is the coupled pressure
  // add any other couplings in a similar manner
  // in other kernels, jvar represents the off diagonal coupled components
  
  // if (jvar == _p_var)
  // {
    // RankTwoTensor dP_dp = -_F[_qp].det() * _F_inv[_qp].transpose();
    // return gradTest(_alpha).doubleContraction(dP_dp);
  // }




  // If jvar corresponds to displacement, use MOOSE's structure for displacement coupling
  // jvar is the coupled displacement
  // such that jvar != the displacement component this kernel acts on
  
  for (unsigned int beta = 0; beta < _ndisp; beta++)
  {
    if (jvar == _disp_nums[beta])
	{
        // Off-Diagonal Terms of the displacement calculation, i.e A != B -> _alpha != _beta
		auto grad_NA = _grad_test[_alpha][_qp];
		auto NA = _test[_alpha][_qp];
		auto grad_NB = _grad_phi[_alpha][_qp]; 
		auto NB = _phi[beta][_qp];	
		  
		RankTwoTensor P = _pk1[_qp];
		RankFourTensor dP_dF = _dpk1[_qp];
		int i = _alpha;
		int k = beta;	
		  
		  
		Real jacobian_ik = 0.0;

		for (unsigned int J = 0; J < _ndisp; ++J)
		{
			for (unsigned int L = 0; L < _ndisp; ++L) 
			{
				jacobian_ik += grad_NA(J) * dP_dF(i, J, k, L) * grad_NB(L);
			}
		}
	}
  }



  return 0;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////






