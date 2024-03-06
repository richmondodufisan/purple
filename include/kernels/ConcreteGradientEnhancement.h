#pragma once

#include "ADKernel.h"
#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>

class ConcreteGradientEnhancement : public DerivativeMaterialInterface<ADKernel>
{
  public:
    static InputParameters validParams();
    ConcreteGradientEnhancement(const InputParameters & parameters);

  protected:
    virtual ADReal computeQpResidual() override;
	
	/// Coupled displacement variables
    unsigned int _ndisp;
    /// Displacement variables IDs
    std::vector<unsigned int> _disp_var;

    /// Material Properties
    const ADMaterialProperty<Real> & _len_scale;
	
	const ADMaterialProperty<Real> & _kappa;

    /// Base name of the material system that this kernel applies to
    const std::string _base_name;
	
    /// Number of dims
    unsigned n_dim;
};