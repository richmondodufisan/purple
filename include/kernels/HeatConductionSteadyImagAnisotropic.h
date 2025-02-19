#pragma once

#include "ADKernel.h"
#include <cmath>
#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>

class HeatConductionSteadyImagAnisotropic : public DerivativeMaterialInterface<ADKernel>
{
  public:
    static InputParameters validParams();
    HeatConductionSteadyImagAnisotropic(const InputParameters & parameters);

  protected:
    virtual ADReal computeQpResidual() override;

    // Base name of the material system that this kernel applies to if needed
    const std::string _base_name;

    // Parameters
	
	const ADVariableValue & _X;
	
	const ADMaterialProperty<RankTwoTensor> & _kappa;
	const ADMaterialProperty<Real> & _c;
	const ADMaterialProperty<Real> & _omega;
	const ADMaterialProperty<Real> & _rho;
};
