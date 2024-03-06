#pragma once

#include "ADKernel.h"
#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>

class ConcreteGradientDamageMomentum : public DerivativeMaterialInterface<ADKernel>
{
  public:
    static InputParameters validParams();
    ConcreteGradientDamageMomentum(const InputParameters & parameters);

  protected:
    virtual ADReal computeQpResidual() override;

    /// Base name of the material system that this kernel applies to
    const std::string _base_name;

    /// The stress tensor that the divergence operator operates on
    const ADMaterialProperty<RankTwoTensor> & _stress;
    const ADMaterialProperty<RankFourTensor> & _cto;
    const ADMaterialProperty<RankTwoTensor> & _strain;

    /// An integer corresponding to the direction this kernel acts in
    const unsigned int _component_disp;

    /// Coupled displacement variables
    unsigned int _ndisp;

    /// Displacement variables IDs
    std::vector<unsigned int> _disp_var;

	const ADMaterialProperty<Real> & _D;

    /// Number of dims
    unsigned n_dim;
};
