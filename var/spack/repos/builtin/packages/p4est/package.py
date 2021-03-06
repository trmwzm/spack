##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class P4est(AutotoolsPackage):
    """Dynamic management of a collection (a forest) of adaptive octrees in
    parallel"""
    homepage = "http://www.p4est.org"
    url      = "http://p4est.github.io/release/p4est-1.1.tar.gz"

    maintainers = ['davydden']

    version('2.0', 'c522c5b69896aab39aa5a81399372a19a6b03fc6200d2d5d677d9a22fe31029a')
    version('1.1', '37ba7f4410958cfb38a2140339dbf64f')

    variant('openmp', default=False, description='Enable OpenMP')

    # build dependencies
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool@2.4.2:', type='build')

    # other dependencies
    depends_on('mpi')
    depends_on('zlib')

    # from sc upstream, correct the default libraries
    patch('https://github.com/cburstedde/libsc/commit/b506aab224b988fec210cc212469f2c4f58b2d04.patch',
          sha256='e9418b1a9347a409be241cd185519b31950e42a7f55b6fb80ce53097657098ee',
          working_dir='sc')
    patch('https://github.com/cburstedde/libsc/commit/b45a51a7ef97883a3d4dcbd05cb2c77890a76f75.patch',
          sha256='8fb829e34e3a1e28afdd6e56e0bdc1d377af569b7ccb9e9d8da0eeb5829ed27e',
          working_dir='sc')

    def autoreconf(self, spec, prefix):
        bootstrap = Executable('./bootstrap')
        bootstrap()

    def configure_args(self):
        args = [
            '--enable-mpi',
            '--enable-shared',
            '--disable-vtk-binary',
            '--without-blas',
            'CPPFLAGS=-DSC_LOG_PRIORITY=SC_LP_ESSENTIAL',
            'CFLAGS=-O2',
            'CC=%s'  % self.spec['mpi'].mpicc,
            'CXX=%s' % self.spec['mpi'].mpicxx,
            'FC=%s'  % self.spec['mpi'].mpifc,
            'F77=%s' % self.spec['mpi'].mpif77
        ]

        if '+openmp' in self.spec:
            try:
                args.append(
                    '--enable-openmp={0}'.format(self.compiler.openmp_flag))
            except UnsupportedCompilerFlag:
                args.append('--enable-openmp')
        else:
            args.append('--disable-openmp')

        return args
