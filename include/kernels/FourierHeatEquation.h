#pragma once

#include "ADKernel.h"
#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>

class FourierHeatEquation : public DerivativeMaterialInterface<ADKernel>
{
  public:
    static InputParameters validParams();
    FourierHeatEquation(const InputParameters & parameters);

  protected:
    virtual ADReal computeQpResidual() override;

    // Base name of the material system that this kernel applies to if needed
    const std::string _base_name;

    // Parameters
    const unsigned int _component_flux;
	
	const ADVariableValue & _temp;
	
	const ADMaterialProperty<Real> & _kappa;
};
