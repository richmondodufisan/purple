/* ---------------------------------------------------------------------
 * Author - Matthias Neuner matthias.neuner@uibk.ac.at
 * ---------------------------------------------------------------------
 */

#include "TLIncompressibilityPressure.h"
#include "DerivativeMaterialInterface.h"

registerMooseObject("purpleApp", TLIncompressibilityPressure);

InputParameters
TLIncompressibilityPressure::validParams()
{
  InputParameters params = Kernel::validParams();
  params.addClassDescription("Variation of potential energy wrt pressure");
  
  params.addParam<std::string>("base_name", "Material property base name");
  params.addRequiredCoupledVar("displacements",
                               "The string of displacements suitable for the problem statement");
							   
  return params;
}

TLIncompressibilityPressure::TLIncompressibilityPressure(const InputParameters & parameters)
  : DerivativeMaterialInterface<Kernel>(parameters),
  
  
    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),



    _ndisp(coupledComponents("displacements")),
    _disp_var(_ndisp),
	
	_F(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient"))        
	
	
{
  // Do the vector coupling of the displacements
  for (unsigned int i = 0; i < _ndisp; i++)
    _disp_var[i] = coupled("displacements", i);

  // We need to use identical discretizations for all displacement components
  auto order_x = getVar("displacements", 0)->order();
  for (unsigned int i = 1; i < _ndisp; i++)
  {
    if (getVar("displacements", i)->order() != order_x)
      mooseError("The Lagrangian StressDivergence kernels require equal "
                 "order interpolation for all displacements.");
  }
}

Real
TLIncompressibilityPressure::computeQpResidual()
{
  // Implement residual here
  const auto & dNA_dX = _grad_test[_i][_qp];	// gradient of pressure test shape function
  const auto & NA = _test[_i][_qp];				// pressure test shape function
  const auto & p = _u[_qp];						// pressure
  
  
  const auto & F = _F[_qp];
  const auto & F_inv = F.inverse();
  const auto & Jac = F.det();
  
  auto kappa = ((2 * 100000) * (1 + 0.49))/(3 * (1 - (2 * 0.49)));
  
  
  
  // Incompressibility ln(J)
  // Real residual_A = std::log(Jac) * NA;
  
  // Incompressibility (1 - J)
  // Real residual_A = (1 - Jac) * NA;
  
  // Incompressibility (1 - J) with p/kappa stabilization
  Real residual_A = ((1 - Jac - (p/kappa)) * NA) ;

  return residual_A;
}

Real
TLIncompressibilityPressure::computeQpJacobian()
{
  return computeQpJacobianPressure();
}

Real
TLIncompressibilityPressure::computeQpOffDiagJacobian(unsigned int jvar)
{
  for (unsigned int j = 0; j < _ndisp; ++j)
    if (jvar == _disp_var[j])
      return computeQpJacobianDisplacement(j);

  mooseError("Jacobian for unknown variable requested");
  return 0.0;
}

Real
TLIncompressibilityPressure::computeQpJacobianDisplacement(unsigned int comp_k)
{
  // Implement here

  const auto & dNA_dX = _grad_test[_i][_qp];
  const auto & dNB_dX = _grad_phi[_j][_qp];
  const auto & NA = _test[_i][_qp];
  const auto & NB = _phi[_j][_qp];

  const auto & F = _F[_qp];
  const auto & F_inv = F.inverse();
  const auto & Jac = F.det();

  const auto k = comp_k;


  Real dResidual_A_dNodeDisplacement_Bk = 0.0;
  
  for (int L = 0;  L < _ndisp; ++L)
  {
	// Incompressibility ln(J)
    // dResidual_A_dNodeDisplacement_Bk += dNB_dX(L) * F_inv(L, k) * NA;
	
	// Incompressibility (1 - J)
    dResidual_A_dNodeDisplacement_Bk += -dNB_dX(L) * Jac * F_inv(L, k) * NA;
  }  


  return dResidual_A_dNodeDisplacement_Bk;
}

Real
TLIncompressibilityPressure::computeQpJacobianPressure()
{
  const auto & dNA_dX = _grad_test[_i][_qp];	// gradient of pressure test shape function
  const auto & NA = _test[_i][_qp];				// pressure test shape function
  const auto & dNB_dX = _grad_phi[_j][_qp];
  const auto & NB = _phi[_j][_qp];
  const auto & p = _u[_qp];						// pressure
  

  const auto & F = _F[_qp];
  const auto & F_inv = F.inverse();
  const auto & Jac = F.det();

  auto kappa = ((2 * 100000) * (1 + 0.49))/(3 * (1 - (2 * 0.49)));
  
  // const auto & F = _F[_qp];
  // const auto & F_inv = F.inverse();
  // const auto & Jac = F.det();


  // Residual has no p dependence
  // Real dResidual_A_dPressure_B = 0.0;
  
  // Incompressibility (1 - J) with p/kappa stabilization
  Real dResidual_A_dPressure_B = -(NB/kappa) * NA;

  return dResidual_A_dPressure_B;
}
