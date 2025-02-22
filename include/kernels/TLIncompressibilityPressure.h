#pragma once

#include "Kernel.h"
#include "DerivativeMaterialInterface.h"


class TLIncompressibilityPressure : public DerivativeMaterialInterface<Kernel>
{
public:
  static InputParameters validParams();

  TLIncompressibilityPressure(const InputParameters & parameters);

protected:
  virtual Real computeQpResidual() override;
  virtual Real computeQpJacobian() override;
  virtual Real computeQpOffDiagJacobian(unsigned int jvar) override;

  Real computeQpJacobianDisplacement(unsigned int comp_k);
  Real computeQpJacobianPressure();

  /// Base name of the material system that this kernel applies to
  const std::string _base_name;

  /// Coupled displacement variables
  unsigned int _ndisp;
  /// Displacement variables IDs
  std::vector<unsigned int> _disp_var;
  
  /// The deformation gradient
  const MaterialProperty<RankTwoTensor> & _F;
};
